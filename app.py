import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from services.UsuarioService import UsuarioService
from services.EstudianteService import EstudianteService
from services.AsignaturaService import AsignaturaService
from services.MatriculaService import MatriculaService

from domain.modelos.Estudiante import EstudianteCreate, EstudianteUpdate
from domain.modelos.Asignatura import AsignaturaCreate, AsignaturaUpdate

app = FastAPI(title="Gestión Académica - Examen")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY","cambia-en-produccion"))

base_dir = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

usuario_service = UsuarioService()
estudiante_service = EstudianteService()
asignatura_service = AsignaturaService()
matricula_service = MatriculaService()


async def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    user = usuario_service.get_by_id(user_id)
    return user


async def require_auth(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    return user


async def require_admin(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    if not user.es_admin:
        raise HTTPException(status_code=403, detail="No autorizado")
    return user


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    return RedirectResponse(url='/estudiantes', status_code=303)


@app.get('/login', response_class=HTMLResponse)
async def login_get(request: Request):
    if request.session.get('user_id'):
        return RedirectResponse(url='/', status_code=303)
    return templates.TemplateResponse('login.html', {'request': request, 'error': request.query_params.get('error')})


@app.post('/login')
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    user = usuario_service.authenticate(username, password)
    if not user:
        return RedirectResponse(url='/login?error=Credenciales incorrectas', status_code=303)
    request.session['user_id'] = user['id']
    request.session['username'] = user['username']
    request.session['is_admin'] = bool(user.get('es_admin'))
    return RedirectResponse(url='/', status_code=303)


@app.get('/logout')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url='/login', status_code=303)


# Estudiantes
@app.get('/estudiantes', response_class=HTMLResponse)
async def estudiantes_list(request: Request, user=Depends(require_auth)):
    estudiantes = estudiante_service.get_all()
    return templates.TemplateResponse('estudiantes_list.html', {'request': request, 'estudiantes': estudiantes, 'user': user, 'success': request.query_params.get('success'), 'error': request.query_params.get('error')})


@app.get('/estudiantes/nuevo', response_class=HTMLResponse)
async def estudiante_new_get(request: Request, user=Depends(require_admin)):
    return templates.TemplateResponse('estudiante_form.html', {'request': request, 'estudiante': None, 'user': user})


@app.post('/estudiantes/nuevo')
async def estudiante_new_post(user=Depends(require_admin), nombre_completo: str = Form(...), dni: str = Form(...), email: str = Form(...), fecha_nacimiento: str = Form(None), titulacion: str = Form(None)):
    est = EstudianteCreate(nombre_completo=nombre_completo, dni=dni, email=email, fecha_nacimiento=fecha_nacimiento, titulacion=titulacion)
    estudiante_service.create(est)
    return RedirectResponse(url='/estudiantes?success=Estudiante creado', status_code=303)


@app.get('/estudiantes/{id}', response_class=HTMLResponse)
async def estudiante_detalle(id: int, request: Request, user=Depends(require_auth)):
    estudiante = estudiante_service.get_by_id(id)
    if not estudiante:
        raise HTTPException(status_code=404, detail='Estudiante no encontrado')
    asignaturas = matricula_service.get_asignaturas_de_estudiante(id)
    disponibles = asignatura_service.get_all()
    # excluir las ya asignadas
    asign_disponibles = [a for a in disponibles if not any(sa.id == a.id for sa in asignaturas)]
    return templates.TemplateResponse('estudiante_detalle.html', {'request': request, 'estudiante': estudiante, 'asignaturas': asignaturas, 'disponibles': asign_disponibles, 'user': user})


@app.post('/estudiantes/{id}/asignar')
async def estudiante_asignar(id: int, asignatura_id: int = Form(...), anio_academico: str = Form(None), user=Depends(require_admin)):
    matricula_service.asignar(id, int(asignatura_id), anio_academico)
    return RedirectResponse(url=f'/estudiantes/{id}?success=Asignatura asignada', status_code=303)


@app.post('/estudiantes/{id}/quitar')
async def estudiante_quitar(id: int, asignatura_id: int = Form(...), user=Depends(require_admin)):
    matricula_service.quitar(id, int(asignatura_id))
    return RedirectResponse(url=f'/estudiantes/{id}?success=Asignatura eliminada', status_code=303)


@app.get('/estudiantes/{id}/editar', response_class=HTMLResponse)
async def estudiante_edit_get(id: int, request: Request, user=Depends(require_admin)):
    estudiante = estudiante_service.get_by_id(id)
    return templates.TemplateResponse('estudiante_form.html', {'request': request, 'estudiante': estudiante, 'user': user})


@app.post('/estudiantes/{id}/editar')
async def estudiante_edit_post(id: int, user=Depends(require_admin), nombre_completo: str = Form(...), dni: str = Form(...), email: str = Form(...), fecha_nacimiento: str = Form(None), titulacion: str = Form(None)):
    est = EstudianteUpdate(nombre_completo=nombre_completo, dni=dni, email=email, fecha_nacimiento=fecha_nacimiento, titulacion=titulacion)
    estudiante_service.update(id, est)
    return RedirectResponse(url='/estudiantes?success=Estudiante actualizado', status_code=303)


@app.post('/estudiantes/{id}/borrar')
async def estudiante_borrar(id: int, user=Depends(require_admin)):
    try:
        estudiante_service.delete(id)
        return RedirectResponse(url='/estudiantes?success=Estudiante borrado', status_code=303)
    except Exception:
        return RedirectResponse(url=f'/estudiantes?error=No se puede borrar: tiene matrículas', status_code=303)


# Asignaturas
@app.get('/asignaturas', response_class=HTMLResponse)
async def asignaturas_list(request: Request, user=Depends(require_auth)):
    asignaturas = asignatura_service.get_all()
    return templates.TemplateResponse('asignaturas_list.html', {'request': request, 'asignaturas': asignaturas, 'user': user, 'success': request.query_params.get('success'), 'error': request.query_params.get('error')})


@app.get('/asignaturas/nueva', response_class=HTMLResponse)
async def asignatura_new_get(request: Request, user=Depends(require_admin)):
    return templates.TemplateResponse('asignatura_form.html', {'request': request, 'asignatura': None, 'user': user})


@app.post('/asignaturas/nueva')
async def asignatura_new_post(user=Depends(require_admin), nombre: str = Form(...), codigo: str = Form(...), creditos: int = Form(...), departamento: str = Form(None), cuatrimestre: str = Form(None)):
    a = AsignaturaCreate(nombre=nombre, codigo=codigo, creditos=creditos, departamento=departamento, cuatrimestre=cuatrimestre)
    asignatura_service.create(a)
    return RedirectResponse(url='/asignaturas?success=Asignatura creada', status_code=303)


@app.get('/asignaturas/{id}', response_class=HTMLResponse)
async def asignatura_detalle(id: int, request: Request, user=Depends(require_auth)):
    asignatura = asignatura_service.get_by_id(id)
    if not asignatura:
        raise HTTPException(status_code=404, detail='Asignatura no encontrada')
    estudiantes = matricula_service.get_estudiantes_de_asignatura(id)
    return templates.TemplateResponse('asignatura_detalle.html', {'request': request, 'asignatura': asignatura, 'estudiantes': estudiantes, 'user': user})


@app.get('/asignaturas/{id}/editar', response_class=HTMLResponse)
async def asignatura_edit_get(id: int, request: Request, user=Depends(require_admin)):
    asignatura = asignatura_service.get_by_id(id)
    return templates.TemplateResponse('asignatura_form.html', {'request': request, 'asignatura': asignatura, 'user': user})


@app.post('/asignaturas/{id}/editar')
async def asignatura_edit_post(id: int, user=Depends(require_admin), nombre: str = Form(...), codigo: str = Form(...), creditos: int = Form(...), departamento: str = Form(None), cuatrimestre: str = Form(None)):
    a = AsignaturaUpdate(nombre=nombre, codigo=codigo, creditos=creditos, departamento=departamento, cuatrimestre=cuatrimestre)
    asignatura_service.update(id, a)
    return RedirectResponse(url='/asignaturas?success=Asignatura actualizada', status_code=303)


@app.post('/asignaturas/{id}/borrar')
async def asignatura_borrar(id: int, user=Depends(require_admin)):
    try:
        asignatura_service.delete(id)
        return RedirectResponse(url='/asignaturas?success=Asignatura borrada', status_code=303)
    except Exception:
        return RedirectResponse(url=f'/asignaturas?error=No se puede borrar: tiene matrículas', status_code=303)


# --- Gestión centralizada de Matrículas (N-M) ---
@app.get('/matriculas', response_class=HTMLResponse)
async def matriculas_list(request: Request, user=Depends(require_auth)):
    matriculas = matricula_service.get_all()
    estudiantes = estudiante_service.get_all()
    asignaturas = asignatura_service.get_all()
    return templates.TemplateResponse('matriculas_list.html', {
        'request': request,
        'matriculas': matriculas,
        'estudiantes': estudiantes,
        'asignaturas': asignaturas,
        'user': user,
        'success': request.query_params.get('success'),
        'error': request.query_params.get('error'),
    })


@app.post('/matriculas/nueva')
async def matricula_nueva(estudiante_id: int = Form(...), asignatura_id: int = Form(...), anio_academico: str = Form(None), user=Depends(require_admin)):
    if not matricula_service.existe_matricula(estudiante_id, asignatura_id):
        matricula_service.asignar(estudiante_id, asignatura_id, anio_academico)
        return RedirectResponse(url='/matriculas?success=Matrícula creada', status_code=303)
    return RedirectResponse(url='/matriculas?error=Matrícula ya existe', status_code=303)


@app.post('/matriculas/{estudiante_id}/{asignatura_id}/borrar')
async def matricula_borrar(estudiante_id: int, asignatura_id: int, user=Depends(require_admin)):
    matricula_service.quitar(estudiante_id, asignatura_id)
    return RedirectResponse(url='/matriculas?success=Matrícula eliminada', status_code=303)

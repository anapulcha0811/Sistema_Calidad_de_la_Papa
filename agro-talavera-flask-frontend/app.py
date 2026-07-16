# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'super_secret_agro_key'

BASE_API_URL = "http://localhost:8000/api"

@app.route('/')
def index():
    if 'token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('username')
        password = request.form.get('password')
        
        try:
            res = requests.post(f"{BASE_API_URL}/auth/login", json={"usuario": usuario, "password": password})
            data = res.json()
            if res.status_code == 200 and data.get('status') == 'ok':
                session['token'] = 'dummy_token'
                session['usuario'] = usuario
                session['rol'] = data.get('rol', 'operador')
                return redirect(url_for('dashboard'))
            else:
                flash('Credenciales inválidas', 'error')
        except Exception as e:
            flash('Error de conexión con el backend', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/cu5')
def cu5():
    if 'token' not in session: return redirect(url_for('login'))
    
    try:
        res = requests.get(f"{BASE_API_URL}/lotes")
        lotes = res.json() if res.status_code == 200 else []
    except:
        lotes = []
        
    return render_template('cu5.html', usuario=session['usuario'], rol=session.get('rol'), current_view='cu5', lotes=lotes)

@app.route('/cu6')
def cu6():
    if 'token' not in session: return redirect(url_for('login'))
    
    try:
        res = requests.get(f"{BASE_API_URL}/lotes")
        lotes = res.json() if res.status_code == 200 else []
    except:
        lotes = []
        
    return render_template('cu6.html', usuario=session['usuario'], rol=session.get('rol'), current_view='cu6', lotes=lotes)

@app.route('/cu7')
def cu7():
    if 'token' not in session: return redirect(url_for('login'))
    
    try:
        res = requests.get(f"{BASE_API_URL}/lotes")
        lotes = res.json() if res.status_code == 200 else []
    except:
        lotes = []
        
    return render_template('cu7.html', usuario=session['usuario'], rol=session.get('rol'), current_view='cu7', lotes=lotes)

@app.route('/dashboard')
def dashboard():
    if 'token' not in session: return redirect(url_for('login'))
    
    try:
        res = requests.get(f"{BASE_API_URL}/reportes/dashboard")
        data = res.json() if res.status_code == 200 else {}
    except:
        data = {}
        
    return render_template('dashboard.html', usuario=session['usuario'], rol=session.get('rol'), current_view='dashboard', data=data)

@app.route('/padron', methods=['GET', 'POST'])
def padron():
    if 'token' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        # Registrar nuevo lote
        data = {
            "codigo": request.form.get("codigo"),
            "nombre": request.form.get("nombre"),
            "cantidad_lote": float(request.form.get("cantidad_lote", 0)),
            "fecha_ingreso": request.form.get("fecha_ingreso"),
            "tipo_producto": request.form.get("tipo_producto"),
            "cod_inspeccion": request.form.get("cod_inspeccion")
        }
        res = requests.post(f"{BASE_API_URL}/lotes", json=data)
        if res.status_code == 200:
            flash("Lote registrado correctamente.", "success")
        else:
            flash("Error al registrar lote.", "error")
        return redirect(url_for('padron'))
        
    try:
        res = requests.get(f"{BASE_API_URL}/lotes")
        lotes = res.json() if res.status_code == 200 else []
    except:
        lotes = []
    return render_template('padron.html', usuario=session['usuario'], rol=session.get('rol'), current_view='padron', lotes=lotes)

@app.route('/atributos', methods=['GET', 'POST'])
def atributos():
    if 'token' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            "lote_id": int(request.form.get("lote_id")),
            "codigo": request.form.get("codigo"),
            "cod_atributo": request.form.get("cod_atributo"),
            "descripcion": request.form.get("descripcion"),
            "cualitativo": request.form.get("cualitativo"),
            "unidad_medida": request.form.get("unidad_medida")
        }
        res = requests.post(f"{BASE_API_URL}/caracteristicas", json=data)
        if res.status_code == 200:
            flash("Atributo registrado correctamente.", "success")
        else:
            flash("Error al registrar atributo.", "error")
        return redirect(url_for('atributos'))
        
    try:
        res = requests.get(f"{BASE_API_URL}/lotes")
        lotes = res.json() if res.status_code == 200 else []
    except:
        lotes = []
        
    return render_template('atributos.html', usuario=session['usuario'], rol=session.get('rol'), current_view='atributos', lotes=lotes)

@app.route('/eventos', methods=['GET', 'POST'])
def eventos():
    if 'token' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            "producto_id": int(request.form.get("producto_id")),
            "cod_atributo": request.form.get("cod_atributo"),
            "descripcion": request.form.get("descripcion"),
            "unidad_medida": request.form.get("unidad_medida"),
            "estandar": request.form.get("estandar"),
            "nivel_calidad_p": request.form.get("nivel_calidad_p"),
            "min": float(request.form.get("min")),
            "max": float(request.form.get("max")),
            "tipo_producto": request.form.get("tipo_producto")
        }
        res = requests.post(f"{BASE_API_URL}/eventos", json=data)
        if res.status_code == 200:
            flash("Evento de calidad registrado correctamente.", "success")
        else:
            flash("Error al registrar evento.", "error")
        return redirect(url_for('eventos'))
        
    try:
        res = requests.get(f"{BASE_API_URL}/productos")
        productos = res.json() if res.status_code == 200 else []
    except:
        productos = []
        
    return render_template('eventos.html', usuario=session['usuario'], rol=session.get('rol'), current_view='eventos', productos=productos)

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if 'token' not in session: return redirect(url_for('login'))
    
    metricas = []
    
    if request.method == 'POST':
        data = {
            "lote_id": int(request.form.get("lote_id")),
            "cod_inspeccion": request.form.get("cod_inspeccion"),
            "fecha_control": request.form.get("fecha_control")
        }
        res = requests.post(f"{BASE_API_URL}/evaluacion", json=data)
        if res.status_code == 200:
            metricas = res.json()
            flash(f"Se evaluaron {len(metricas)} atributos automáticamente.", "success")
        else:
            flash(res.json().get('detail', 'Error al registrar evaluación.'), "error")
        
    try:
        res_lotes = requests.get(f"{BASE_API_URL}/lotes")
        lotes = res_lotes.json() if res_lotes.status_code == 200 else []
    except:
        lotes = []
        
    return render_template('evaluacion.html', usuario=session['usuario'], rol=session.get('rol'), current_view='evaluacion', lotes=lotes, metricas=metricas)



@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'token' not in session: return redirect(url_for('login'))
    if session.get('rol') != 'administrador':
        flash('Acceso denegado. Se requieren permisos de Administrador para acceder a Configuración.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = {
            "tipo_producto": request.form.get("tipo_producto"),
            "cod_atributo": request.form.get("cod_atributo"),
            "descripcion": request.form.get("descripcion"),
            "unidad_medida": request.form.get("unidad_medida"),
            "estandar": request.form.get("estandar"),
            "nivel_calidad_p": request.form.get("nivel_calidad_p"),
            "min": float(request.form.get("min")),
            "max": float(request.form.get("max"))
        }
        evento_id = request.form.get("evento_id")
        
        if evento_id:
            res = requests.put(f"{BASE_API_URL}/configuracion/parametros/{evento_id}", json=data)
            if res.status_code == 200:
                flash("Parámetro maestro actualizado correctamente.", "success")
            else:
                flash("Error al actualizar parámetro maestro.", "error")
        else:
            res = requests.post(f"{BASE_API_URL}/configuracion/parametros", json=data)
            if res.status_code == 200:
                flash("Parámetro maestro registrado correctamente.", "success")
            else:
                flash("Error al registrar parámetro maestro.", "error")
        return redirect(url_for('settings'))

    try:
        # Traer todos los parámetros para la tabla de visualización (y edición futura)
        res_params = requests.get(f"{BASE_API_URL}/configuracion/parametros")
        parametros_list = res_params.json() if res_params.status_code == 200 else []
    except:
        parametros_list = []

    return render_template('settings.html', usuario=session['usuario'], rol=session.get('rol'), current_view='settings', parametros=parametros_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

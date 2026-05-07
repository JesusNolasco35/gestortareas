from flask import Flask, render_template, request, redirect, url_for, session, flash
from GestorTareas import GestorTareas
from bson import ObjectId

app = Flask(__name__)
app.secret_key = '12345678'

gestor = GestorTareas()

gestor.crear_usuario("trevi", "juan@gmail.com", "1234")

@app.route('/')
def index():
    return redirect(url_for('inicio'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not first_name or not last_name or not email or not password:
            flash('Todos los campos son obligatorios')
            return redirect(url_for('registro'))
        
        if gestor.usuarios.find_one({"email": email}):
            flash('El correo ya está registrado')
            return redirect(url_for('registro'))
        
        nombre_completo = f"{first_name} {last_name}"
        gestor.usuarios.insert_one({
            "nombre": nombre_completo,
            "email": email,
            "password": password
        })
        
        flash('Registro exitoso. Ahora puedes iniciar sesión')
        return redirect(url_for('inicio'))
    
    return render_template('registro.html')

@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Correo y contraseña son obligatorios')
            return redirect(url_for('inicio'))
        
        usuario = gestor.usuarios.find_one({"email": email})
        
        if usuario and usuario['password'] == password:
            session['user_id'] = str(usuario['_id'])
            session['user_nombre'] = usuario['nombre']
            flash('Inicio de sesión exitoso')
            return redirect(url_for('tareas'))
        else:
            flash('Correo o contraseña incorrectos')
            return redirect(url_for('inicio'))
    
    return render_template('inicio.html')

@app.route('/tareas')
def tareas():
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('inicio'))
    
    # Obtener tareas del usuario actual
    usuario_id = session['user_id']
    tareas_lista = gestor.obtener_tareas_usuario(usuario_id)
    
    return render_template('tareas.html', tareas=tareas_lista)

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('inicio'))
    
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion', '')
    
    if not titulo:
        flash('El título es obligatorio')
        return redirect(url_for('tareas'))
    
    usuario_id = session['user_id']
    gestor.crear_tarea(usuario_id, titulo, descripcion)
    flash('✅ Tarea agregada exitosamente')
    return redirect(url_for('tareas'))

@app.route('/completar_tarea/<tarea_id>')
def completar_tarea(tarea_id):
    if 'user_id' not in session:
        return redirect(url_for('inicio'))
    
    usuario_id = session['user_id']
    
    gestor.tareas.update_one(
        {"_id": ObjectId(tarea_id), "usuario_id": ObjectId(usuario_id)},
        {"$set": {"completada": True, "estado": "completada"}}
    )
    flash('🎉 ¡Tarea completada!')
    return redirect(url_for('tareas'))

@app.route('/editar_tarea/<tarea_id>', methods=['POST'])
def editar_tarea(tarea_id):
    if 'user_id' not in session:
        return redirect(url_for('inicio'))
    
    usuario_id = session['user_id']
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    
    gestor.tareas.update_one(
        {"_id": ObjectId(tarea_id), "usuario_id": ObjectId(usuario_id)},
        {"$set": {"titulo": titulo, "descripcion": descripcion}}
    )
    flash('✏️ Tarea editada exitosamente')
    return redirect(url_for('tareas'))

@app.route('/eliminar_tarea/<tarea_id>')
def eliminar_tarea(tarea_id):
    if 'user_id' not in session:
        return redirect(url_for('inicio'))
    
    usuario_id = session['user_id']
    
    gestor.tareas.delete_one({"_id": ObjectId(tarea_id), "usuario_id": ObjectId(usuario_id)})
    flash('🗑️ Tarea eliminada')
    return redirect(url_for('tareas'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)
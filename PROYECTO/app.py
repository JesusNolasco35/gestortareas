from flask import Flask, render_template, request, redirect, url_for, session, flash
import GestorTareas

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('inicio'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('registro.html')





@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    gestor = GestorTareas ()
    if gestor:
        if gestor.obtener_usuario2("hola@gmail.com", "1234")
            return render_template('inicio.html')
        else:
            pass
    
    
    else:
        render render_template('errorConeccion')






@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    return render_template('recuperar.html')

@app.route('/tareas')
def tareas():
    return render_template('tareas.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)
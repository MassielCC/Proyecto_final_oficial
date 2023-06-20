from flask import Flask, render_template, request, redirect, url_for
from forms import SignupForm, CartaForm, LoginForm, ComentarioForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
# app.config['SECRET_KEY'] = 'pass'

HaIniciado_sesion = False
esAdmin = False
errorSesion= False
@app.route("/")
def index():
    return render_template("index.html", inicioSesion=HaIniciado_sesion, admin=esAdmin)

users=[]
@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    # verificamos cuando el usuario haga click en submit (botón Registrar)
    if form.validate_on_submit():
        # Obtenemos datos del form:
        name = form.name.data
        email = form.email.data
        password = form.password.data
        try:
            with open("lista_usuarios.txt", "a+") as archivo1:
                archivo1.write(f"{name},{email},{password}" + "\n")
        finally:
            archivo1.close()
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        # redigire a la página principal!
        return redirect(url_for('index'))
    # caso contrario, redirige a signup_form con el contenido de form.
    return render_template("/admin/signup_form.html", form=form, inicioSesion=HaIniciado_sesion, admin=esAdmin)

listaPlatos = []
@app.route("/admin/crear_carta/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/crear_carta/<int:post_id>/", methods=['GET', 'POST'])
def crear_carta(post_id):
    formulario = CartaForm()
    # si yo hago click en Enviar, y la validación ha sido correcta:
    if formulario.validate_on_submit():
        nombre = formulario.nombre.data
        descripcion = formulario.descripcion.data
        precio = formulario.precio.data
        print(f'¡Plato agregado! Nombre: {nombre}, Descripción: {descripcion}')
        try:
            with open("platos_carta.txt", "a+") as archivo1:
                archivo1.write(f"{nombre} & {descripcion} & {precio}" + "\n")
        finally:
            archivo1.close()
        return redirect(url_for('index'))
    return render_template("/admin/crear_carta.html", form=formulario, inicioSesion=HaIniciado_sesion, admin=esAdmin)

@app.route("/admin/carta")
def carta():
    return render_template('/admin/carta.html', posts=listaPlatos, inicioSesion=HaIniciado_sesion, admin=esAdmin)

lista_comentarios=[]
@app.route('/admin/comentarios', methods=['GET', 'POST'])
def crear_comentario():
    formulario = ComentarioForm()
    if formulario.validate_on_submit():
        nombre = formulario.nombre.data
        correo = formulario.correo.data
        comentario = formulario.comentario.data
        print(f'¡Comentario creado! Nombre: {nombre}, Correo: {correo}, Comentario: {comentario}')
        try:
            with open("comentarios.txt", "a+") as archivo1:
                archivo1.write(f"{nombre} & {correo} & {comentario}" + "\n")
        finally:
            archivo1.close()
        return redirect(url_for('index'))
    return render_template('/admin/comentarios.html', form=formulario, inicioSesion=HaIniciado_sesion, admin=esAdmin)

@app.route("/admin/ver_comentarios/")
def comentarios():
    return render_template('/admin/ver_comentarios.html', post=lista_comentarios, inicioSesion=HaIniciado_sesion, admin=esAdmin)

@app.route("/admin/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        # tomamos los valores ingresados por teclado en el formulario
        email = form.email.data
        password = form.password.data
        #print('email ingresado: ' +email)
        #print('contraseña ingresada: ' +password)
        # recoro la lista usuarios
        for elemento in users:
            #print(elemento)
            # evaluo el valor de 'usuario' y contraseña en el diccionario vs el ingresado en el formulario
            if elemento['usuario'] == email and elemento['clave'].strip() == password:
                # si cumple imprimimos en pantalla: inicio de sesión correcto!
                print('Inicio de sesión correcto!')
                global HaIniciado_sesion
                HaIniciado_sesion = True
                global errorSesion
                errorSesion = False
                if email == "marelly.colla@upch.pe" or email == "sebastian.saldana@upch.pe":
                    print("Es administrador")
                    global esAdmin
                    esAdmin = True
                break
            else:
                print("Error")
                errorSesion = True

        if(errorSesion):
            return render_template("/admin/login.html", form=form, error=errorSesion)

        return render_template("index.html", inicioSesion=HaIniciado_sesion, admin=esAdmin)
    return render_template("/admin/login.html", form=form)

@app.route("/signout")
def cerrar_sesion():
    global HaIniciado_sesion # indicamos que vamos a modificar el valor de la linea 10
    HaIniciado_sesion = False # modificamos el valor de HaIniciado_sesion a False
    global esAdmin
    esAdmin = False
    # retornamos la página web index.html con HaIniciado_sesion en False
    return render_template('index.html', inicioSesion = HaIniciado_sesion, admin=esAdmin)

if __name__ == '__main__':
    try:
        # lectura del archivo usuarios.txt
        with open("lista_usuarios.txt", "r") as archivo2:
            # en usuarios_ guardamos el contenido de usuarios.txt como una lista de str
            usuarios_ = archivo2.readlines()
            #print("contenido: ", usuarios_)
    except FileNotFoundError:
        print("No se ha creado el archivo")
    finally:
        archivo2.close()
        for u_ in usuarios_:
            # divido en una lista el contenido de cada linea
            info = u_.split(',')
            elemento = {}  # creo el diccionario elemento
            elemento['usuario'] = info[1]  # el key 'usuario' toma el valor del correo
            elemento['clave'] = info[2].strip('\n')  # el key 'clave' guarda la contraseña
            users.append(elemento)
    #Para mostrar Platos en carta
    try:
        with open("platos_carta.txt", "r") as archivo1:
            platos_all = archivo1.readlines()
    finally:
        archivo1.close()
        for line in platos_all:
            elem = line.split('&')
            plato = {}
            plato['nombre'] = elem[0]
            plato['descripcion'] = elem[1]
            plato['precio'] = elem[2].strip('\n')
            listaPlatos.append(plato)

    # Para mostrar comentarios al administrador
    try:
        with open("comentarios.txt", "r") as archivo1:
            comment_all = archivo1.readlines()
            #print(comment_all)
    finally:
        archivo1.close()
        for line in comment_all:
            elem = line.split('&')
            comment = {}
            comment['nombre'] = elem[0]
            comment['correo'] = elem[1]
            comment['texto'] = elem[2].strip('\n')
            lista_comentarios.append(comment)
    app.run(debug=True)

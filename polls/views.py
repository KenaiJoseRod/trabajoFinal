from django.shortcuts import render,redirect
from django.contrib import messages
from polls.models import Contrato, Cliente, Trabajador, Inmueble
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def obtener_datos_formulario():
    clientes = Cliente.objects.all().values('cli_dni')
    trabajadores = Trabajador.objects.all().values('tra_dni')
    inmuebles = Inmueble.objects.all().values('inm_codigo')
    return {'clientes': clientes, 'trabajadores': trabajadores, 'inmuebles': inmuebles}
def obtener_contratos():
    try:
        # Llama al procedimiento almacenado
        with connection.cursor() as cursor:
            cursor.callproc('sp_MostrarContratos')
            results = cursor.fetchall()
        contratos = []
        for row in results:
            contrato = {
                'nombre_contrato': row[0],
                'cnt_codigo': row[1],
                'estado': row[4],
                'nombre_cliente': row[3],
                'nombre_trabajador': row[6],
                'valor_contrato': row[8],
                'fecha_contrato': row[2],
                'tipo_inmueble': row[9],
                'descripcion_inmueble': row[10]
            }
            contratos.append(contrato)
        return contratos
    except Exception as e:
        # Manejo de errores
        raise e
def crear_contrato_desde_fila(row):
    contrato = {
        'nombre_contrato': row[0],
        'cnt_codigo': row[1],
        'estado': row[4],
        'nombre_cliente': row[3],
        'nombre_trabajador': row[6],
        'valor_contrato': row[8],
        'fecha_contrato': row[2],
        'tipo_inmueble': row[9],
        'descripcion_inmueble': row[10]
    }
    return contrato
def indexPage(request):  
    return render(request, 'index.html')

def LogoutPage(request):
    logout(request)
    messages.info(request, "Cierre de sesión con éxito!")
    return redirect('login')

def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            pass1 = request.POST.get('password')
            user = authenticate(request, username=user.username, password=pass1)
            if user is not None:
                messages.success(request, 'Inicio de sesion correcto')
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta')
                return render(request, 'login.html',{'email': email})
        except User.DoesNotExist:
            messages.error(request, ' Email no encontrado')
            


    return render(request, 'login.html')

def SignupPage(request):
    username = ''
    email = ''
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if  User.objects.filter(email=email).exists():
            messages.success(request, ' El correo('+str(email)+') Ya Existe!!')
            return render(request, 'signup.html',{'username': uname})

        elif pass1!=pass2:
            messages.success(request, 'Las Contraseñas no Coinsiden, intentelo de nuevo',)
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            messages.success(request, 'Usuario registrado')

            return redirect('login')
        username = uname


    return render (request,'signup.html', {'username': username, 'email': email})

@login_required(login_url='login')
def HomePage(request):  
    try:
        contratos = obtener_contratos()
        total_contratos = len(contratos)
        datos = {'pro': contratos, 'total_contratos': total_contratos}
        return render(request, 'listado.html', datos)
        # Pasa los resultados a la plantilla HTML
    except Exception as e:
        # Manejo de errores
        return render(request, 'listado.html', {'error': str(e)})
    
@login_required(login_url='login')
def mostrarFormRegistrar(request):
    datos_formulario = obtener_datos_formulario()
    return render(request, 'form_registrar.html', datos_formulario)

@login_required(login_url='login')
def insertarContrato(request):
    if request.method == 'POST':
        cod=request.POST.get('cnt_codigo')
        nom = request.POST.get('cnt_nombre')
        form = request.POST.get('cnt_formapago')
        estado = request.POST.get('estado')
        fecha_firma = request.POST.get('cnt_fechafirma')
        fecha_contrato = request.POST.get('cnt_fechacontrato')
        cliente_id = request.POST.get('cliente')
        trabajador_id = request.POST.get('trabajador')
        inmueble_id = request.POST.get('inmueble')

        # Check if all required fields are provided
        if not all([cod,nom, form, estado, fecha_firma, fecha_contrato, cliente_id, trabajador_id, inmueble_id]):
            messages.error(request, 'Todos los campos son obligatorios.')
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('sp_InsertContrato', [
                        cod,nom, form, fecha_firma, fecha_contrato, estado, cliente_id, trabajador_id, inmueble_id
                    ])
                messages.success(request, 'El contrato se registró correctamente!!')
            except Exception as e:
                messages.error(request, f'Error al registrar el contrato: {str(e)}')

        # Fetch clients and workers for the form
        datos_formulario = obtener_datos_formulario()
        return render(request, 'form_registrar.html', datos_formulario)
    else:
        messages.error(request, 'No se puede procesar la solicitud!!')

        # Fetch clients and workers for the form
        datos_formulario = obtener_datos_formulario()
        return render(request, 'form_registrar.html', datos_formulario)
    
@login_required(login_url='login')    
def mostrarFormActualizar(request, cnt_codigo):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_DetalleContrato', [cnt_codigo])
            pro = cursor.fetchone()

        # Formatea las fechas si es necesario
        if pro:
            pro = {
                'cnt_codigo':pro[0],
                'cnt_nombre':pro[1],
                'cnt_formapago':pro[2],
                'cnt_fechafirma': pro[3].strftime('%Y-%m-%d') if pro[3] else None,
                'cnt_fechacontrato': pro[4].strftime('%Y-%m-%d') if pro[4] else None,
                'cnt_estado':pro[5],
                'cliente_id':pro[6],
                'trabajador_id':pro[8],
                'inmueble_id':pro[7],
            }

        datos = { 'pro' : pro }
        return render(request, 'form_actualizar.html', datos)
        
    except Exception as e:
        # Manejo de errores
        return render(request, 'error.html', {'error': str(e)})
    
@login_required(login_url='login')
def actualizarContrato(request,cnt_codigo):
    if request.method == 'POST':
        # Obtener los datos actualizados del formulario
        cnt_nombre = request.POST['cnt_nombre']
        cnt_formapago = request.POST['cnt_formapago']
        cnt_fechafirma = request.POST['cnt_fechafirma']
        cnt_fechacontrato = request.POST['cnt_fechacontrato']
        cnt_estado = request.POST['cnt_estado']
        cliente_id = request.POST['cliente']
        trabajador_id = request.POST['trabajador']
        inmueble_id = request.POST['inmueble']

        try:
            # Llama al procedimiento almacenado para actualizar el contrato
            with connection.cursor() as cursor:
                cursor.callproc('sp_ActualizarContrato', [
                    cnt_codigo, cnt_nombre, cnt_formapago, cnt_fechafirma, cnt_fechacontrato,
                    cnt_estado, cliente_id, trabajador_id, inmueble_id
                ])
            contratos = obtener_contratos()
            datos = {'pro': contratos, 'r': 'Datos Modificados Correctamente!!'}
            return render(request, 'listado.html', datos)
        except Exception as e:
            # Manejar cualquier error que ocurra durante la actualización
            return render(request, 'error.html', {'error': str(e)})
        
@login_required(login_url='login')
def mostrarbuscador(request):
    return render(request, 'buscador.html')

@login_required(login_url='login')
def buscadorfecha(request):
    if request.method == 'GET':
        fecha_busqueda = request.GET.get('fecha')
        if fecha_busqueda:
            with connection.cursor() as cursor:
                cursor.callproc('sp_MostrarContratosPorFecha',  [fecha_busqueda])
                results = cursor.fetchall()
            contratos = [crear_contrato_desde_fila(row) for row in results]

            total_contratos = len(contratos)
            datos = {'pro': contratos, 'total_contratos': total_contratos}
            return render(request, 'buscador.html', datos)
        else:
            messages.error(request, 'Debe seleccionar una fecha.')
            return render(request, 'buscador.html')
    else:
        return render(request, 'buscador.html')

@login_required(login_url='login')
def eliminarProducto(request, cnt_codigo):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_EliminarContrato', [cnt_codigo])
        messages.success(request, 'Registro eliminado correctamente')
        return redirect(to='home')
    except Exception as e:
        # Manejo de errores
        return render(request, 'error.html', {'error': str(e)})

@login_required(login_url='login')
def mostrarFormContrato(request, estado):
    try:
        # Llama al procedimiento almacenado
        with connection.cursor() as cursor:
            cursor.callproc('sp_MostrarContratosPorEstado', [estado])
            results = cursor.fetchall()

        # Crear lista de contratos
        contratos = [crear_contrato_desde_fila(row) for row in results]

        total_contratos = len(contratos)
        datos = {'pro': contratos, 'total_contratos': total_contratos}
        return render(request, 'form_contrato.html', datos)
    except Exception as e:
        # Manejo de errores
        return render(request, 'error.html', {'error': str(e)})

@login_required(login_url='login')
def mostrarContratoxano(request):
    return render(request, 'form_contratoxano.html')

@login_required(login_url='login')
def buscadoraño(request):
    if request.method == 'GET':
        año = request.GET.get('año')
        if año:
            with connection.cursor() as cursor:
                cursor.callproc('sp_MostrarContratosPorAno',  [año])
                results = cursor.fetchall()
            contratos = [crear_contrato_desde_fila(row) for row in results]

            total_contratos = len(contratos)
            datos = {'pro': contratos, 'total_contratos': total_contratos}
            return render(request, 'form_contratoxano.html', datos)
        else:
            messages.error(request, 'Debe seleccionar una fecha.')
            return render(request, 'form_contratoxano.html')
    else:
        return render(request, 'form_contratoxano.html')

@login_required(login_url='login')
def mostrarContmes(request):
    return render(request, 'form_contMes.html')

@login_required(login_url='login')
def buscadormes(request):
    if request.method == 'GET':
        mes = request.GET.get('mes')
        if mes:
            with connection.cursor() as cursor:
                cursor.callproc('sp_MostrarContratosPorMes',  [mes])
                results = cursor.fetchall()
            contratos = [crear_contrato_desde_fila(row) for row in results]

            total_contratos = len(contratos)
            datos = {'pro': contratos, 'total_contratos': total_contratos}
            return render(request, 'form_contMes.html', datos)
        else:
            messages.error(request, 'Debe seleccionar una fecha.')
            return render(request, 'form_contMes.html')
    else:
        return render(request, 'form_ccontMes.html')

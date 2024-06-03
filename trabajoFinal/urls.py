"""
URL configuration for trabajoFinal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.indexPage,name='index'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),
    path('register/',views.SignupPage,name='signup'),
    path('home/',views.HomePage,name='home'),

    path('form_registrar', views.mostrarFormRegistrar),
    path('insertar', views.insertarContrato),

    path('form_actualizar/<str:cnt_codigo>', views.mostrarFormActualizar),
    path('actualizar/<str:cnt_codigo>', views.actualizarContrato),

    path('form_buscador', views.mostrarbuscador),
    path('buscador', views.buscadorfecha),

    path('eliminar/<str:cnt_codigo>', views.eliminarProducto),

    path('form_contrato/<str:estado>/', views.mostrarFormContrato, name='form_contrato'),

    path('form_conXaño', views.mostrarContratoxano),
    path('buscarXaño', views.buscadoraño),
    
    path('form_conXmes', views.mostrarContmes),
    path('buscarXmes', views.buscadormes)



]

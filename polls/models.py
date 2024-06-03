from django.db import models

# Create your models here.
class Contrato(models.Model):
    cnt_codigo = models.CharField(primary_key=True,max_length=5)
    cnt_nombre=models.CharField(max_length=100)
    cnt_formapago=models.CharField(max_length=20)
    cnt_fechafirma=models.DateField()
    cnt_fechacontrato=models.DateField()
    cnt_estado=models.CharField(max_length=50)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    trabajador = models. ForeignKey('Trabajador', on_delete=models.CASCADE)
    inmueble = models. ForeignKey('Inmueble', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Cliente(models.Model):
    cli_dni =models.IntegerField(max_length=7, primary_key=True, editable=False )
    cli_nombre=models.CharField(max_length=100)
    cli_apellido=models.CharField(max_length=100)
    cli_telefono = models.CharField(max_length=9)
    cli_direccion=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Trabajador (models.Model):
    tra_dni= models.IntegerField (max_length=7, primary_key=True, editable=False)
    tra_nombre=models.CharField(max_length=100)
    tra_apellido=models.CharField(max_length=100)
    tra_telefono = models.CharField(max_length=9)
    tra_direccion=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Inmueble(models.Model):
    inm_codigo = models.CharField(max_length=5, primary_key=True, editable=False)
    inm_tipo=models.CharField(max_length=100)
    inm_valor=models.FloatField()
    inm_estado=models.CharField(max_length=100)
    inm_des=models.CharField(max_length=100)

    def __str__(self):
        return self.name
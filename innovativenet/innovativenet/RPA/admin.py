from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class EmployeeInline(admin.StackedInline):
    model = InformacionPersonal
    verbose_name = 'Informacion personal'


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)


# Register your models here.

admin.site.register(Mantenimiento)
admin.site.register(Cliente)
admin.site.register(Precio)
admin.site.register(Nombre_servicio)
admin.site.register(Cotizacion)
# Register your models here.

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
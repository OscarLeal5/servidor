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
admin.site.register(Cliente)
admin.site.register(Precio)
admin.site.register(Precio_centro)
admin.site.register(Nombre_servicio)
admin.site.register(Nombre_servicio_CCTV)
admin.site.register(Nombre_servicio_CA)

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ("titulonombre", "cotizacion","cliente")

class CotizacionAdmin(admin.ModelAdmin):
    list_display = ("titulo","cliente")

admin.site.register(Mantenimiento,MantenimientoAdmin)
admin.site.register(Mantenimiento_CCTV,MantenimientoAdmin)
admin.site.register(Mantenimiento_CA,MantenimientoAdmin)

admin.site.register(Cotizacion,CotizacionAdmin)
admin.site.register(Cotizacion_CCTV,CotizacionAdmin)
admin.site.register(Cotizacion_CA,CotizacionAdmin)
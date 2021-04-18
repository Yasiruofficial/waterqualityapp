from django.contrib import admin

# Register your models here.
from api.models import Location, Subscriber, Data, Device

admin.site.register(Location)
admin.site.register(Device)
admin.site.register(Data)
admin.site.register(Subscriber)
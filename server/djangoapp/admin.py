from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('carmake', 'dealer_id', 'model','car_type', 'year')

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['carmake', 'description', 'country']
    list_display = ('carmake', 'country', 'description')
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel,CarModelAdmin)

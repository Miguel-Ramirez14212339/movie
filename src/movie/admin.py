from django.contrib import admin
from .models import  Movie

# Register your models here.

class MovieModelAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'year',
        'studio',
        'slug',
        'genre',
        'active',
        'created',
        'updated',
        'timestamp',
        'get_age'
        ]

    readonly_fields = ['created','updated','slug','timestamp','get_age']

    def get_age(self, obj, *args, **kwargs):
        return str(obj.age)

    class Meta:
        model = Movie

admin.site.register(Movie, MovieModelAdmin)

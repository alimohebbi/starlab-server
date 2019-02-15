from django.contrib import admin

# Register your models here.
from main_api.models import News, People

admin.site.register(News)
admin.site.register(People)

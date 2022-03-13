from sqlite3 import Time
from django.contrib import admin
from time_management_app.models import TimeManagement, Information

# Register your models here.
admin.site.register(TimeManagement)
admin.site.register(Information)

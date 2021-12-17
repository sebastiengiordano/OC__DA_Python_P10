from django.contrib import admin

from .models import (
    Projects, Contributors,
    Issues)

admin.site.register(Projects)
admin.site.register(Contributors)
admin.site.register(Issues)

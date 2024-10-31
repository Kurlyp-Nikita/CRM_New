from django.contrib import admin
from .models import UserProfile, Lead, Client


admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Client)

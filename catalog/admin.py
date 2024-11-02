from django.contrib import admin
from .models import UserProfile, Lead, Client, Team, Plan


admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Client)
admin.site.register(Team)
admin.site.register(Plan)

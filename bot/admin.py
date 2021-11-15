from django.contrib import admin
from .models import PersonalOrder, TelegramUser

admin.site.register(TelegramUser)
admin.site.register(PersonalOrder)

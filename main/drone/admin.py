from django.contrib import admin
from .models import RegisteredUsers, UnRegisteredUsers, tickets
# Register your models here.
admin.site.register(RegisteredUsers)
admin.site.register(UnRegisteredUsers)
admin.site.register(tickets)



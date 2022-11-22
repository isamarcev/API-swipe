from django.contrib import admin
from users.models import Contact, CustomUser

# Register your models here.
admin.site.register(Contact)
admin.site.register(CustomUser)

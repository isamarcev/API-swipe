from django.contrib import admin
from users.models import Contact, CustomUser, Subscription, Notary, Message

# Register your models here.
admin.site.register(Contact)
admin.site.register(CustomUser)
admin.site.register(Subscription)
admin.site.register(Message)

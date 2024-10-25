from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(EventInformation)
admin.site.register(FormData)
admin.site.register(DraftModel)

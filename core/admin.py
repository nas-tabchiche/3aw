from django.contrib import admin
from .models import Policy


class PolicyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Policy, PolicyAdmin)

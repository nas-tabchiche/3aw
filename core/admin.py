from django.contrib import admin
from .models import Instance, Rule


class InstanceAdmin(admin.ModelAdmin):
    list_display = ("host", "port")


class RuleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Instance, InstanceAdmin)
admin.site.register(Rule, RuleAdmin)

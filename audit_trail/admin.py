from django.contrib import admin

from audit_trail.models import AuditLog
class AuditLogAdmin(admin.ModelAdmin):
    list_display= ('content_type','object_id','content_object',)
    list_filter = ('content_type',)

admin.site.register(AuditLog,AuditLogAdmin)



from django.contrib import admin
from .models import Extract 
from django.shortcuts import redirect 


class ExtractAdmin(admin.ModelAdmin):
    readonly_fields = ('executed_on',)
    def response_change(self, request, obj):
        if "extract" in request.POST:
            if not obj.was_executed_before:
                try:    
                    obj.extract()
                    obj.was_executed_before = True
                    obj.save()
                except (ValueError, TypeError):
                    pass
            return redirect(".")
        # if we didn't find 'execute' in POST data
        return  super().response_change(request, obj)

admin.site.register(Extract, ExtractAdmin)

from django.contrib import admin

# Register your models here.
from .models import User, Company, Site_Slug

'''
# Minimal registration of Models.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Site_Slug)
'''
admin.site.register(Site_Slug)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('get_lastname', 'email', 'company', 'queries')
    filter = ('company')

    def get_lastname(self,obj):
        return obj.user.last_name
    get_lastname.short_description = 'User'
    get_lastname.admin_order_field = 'user__last_name'

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'display_slug')
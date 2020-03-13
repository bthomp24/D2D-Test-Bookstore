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
    list_display = ('name', 'email', 'company', 'queries')
    filter = ('company')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'display_slug')
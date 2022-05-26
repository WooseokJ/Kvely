from django.contrib import admin

from board_real.models import File

from .models import File
# Register your models here.

# @admin.register(File)
# class Vendor_infoAdmin(admin.ModelAdmin):
    # list_display = ('ven_id', 'ven_name', 'ven_tel', 'ven_fax', 'ven_email')
    # list_filter = ('ven_id',)
    # search_fields = ('ven_name', 'ven_id')
admin.site.register(File)

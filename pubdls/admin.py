from django.contrib import admin

from pubdls.models import Regnum

# Register your models here.

# admin.site.register(Regnum)


@admin.register(Regnum)
class RegnumAdmin(admin.ModelAdmin):
    list_display = ('reg_num', 'reg_date', 'doc_type', 'rp_number', 'drug_name', 'serial_num', 'manufacture')
    list_filter = ['reg_date']
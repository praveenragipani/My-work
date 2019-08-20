from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from asset_mgmt.models import AssetCatalog


# Register your models here.


class AssetCatalogAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description', 'asset_type', 'business_owner', 'analytic_type', 'modified_at')
    list_display_links = ('name',)
#    list_editable = ('description',)
    list_per_page = 200
    search_fields = ('name', 'description')
    list_filter = ('asset_type', 'analytic_type', 'asset_studio')


admin.site.register(AssetCatalog, AssetCatalogAdmin)

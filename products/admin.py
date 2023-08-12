from django.contrib import admin
from products.models import Categorie, Stock, SaleHistory, SupplyHistory
from products.forms import StockCreateForm


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom']
    list_per_page = 20


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id','reference', 'designation', 'categorie', 'quantite', 'seuil_alert', 'prix_achat', 'pourcentage', 'prix_vente', 'date_creation']
    list_display_links = ['reference', 'designation']
    search_fields = ['reference', 'designation', 'categorie']
    #list_editable = ['seuil_alert']
    date_hierarchy = "date_creation"
    list_filter = ['categorie']
    #form = StockCreateForm
    list_per_page = 15


@admin.register(SaleHistory)
class SaleHistoryAdmin(admin.ModelAdmin):
    list_display = ['reference', 'designation', 'categorie', 'quantite_vendu', 'prix_unitaire', 'date_mise_a_jour', 'get_total_price']
    list_display_links = ['reference', 'designation']
    search_fields = ['reference', 'designation', 'categorie']
    #list_editable = ['seuil_alert']
    list_filter = ['categorie']
    list_per_page = 15


@admin.register(SupplyHistory)
class SupplyHistoryAdmin(admin.ModelAdmin):
    list_display = ['reference', 'designation', 'categorie', 'quantite_recu', 'prix_unitaire', 'date_mise_a_jour', 'get_total_price']
    list_display_links = ['reference', 'designation']
    search_fields = ['reference', 'designation', 'categorie']
    #list_editable = ['seuil_alert']
    list_filter = ['categorie']
    list_per_page = 15

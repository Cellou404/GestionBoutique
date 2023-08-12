from django_tables2 import tables
from .models import Stock

class StockTable(tables.Table):
    class Meta:
        model = Stock
        fields = ['reference', 'designation','categorie', 'quantite', 'prix_unitaire', 'seuil_alert', 'date_mise_a_jour']

from django.shortcuts import render, redirect
from django.db.models import F, Sum, Count
from django.db.models.functions import ExtractWeekDay, Coalesce
from django.utils import timezone
from datetime import datetime, timedelta, date
import pytz
from django.views.decorators.cache import cache_page
from django.contrib import messages

from products.models import Stock, SaleHistory, SupplyHistory

from products.views import addItem # Import addItem view
from suppliers.views import create_supplier

from products.forms import StockCreateForm
from suppliers.forms import SupplierCreateUpdateForm


def dashboard(request):
    # Somme Total des Ventes et celle des Achats
    total_sale = SaleHistory.objects.aggregate(
        ventes=Sum(F('prix_unitaire') * F('quantite_vendu'))
    )

    total_supply = SupplyHistory.objects.aggregate(
        achats=Sum(F('prix_unitaire') * F('quantite_recu'))
    )
    # Compter le nombre d'article en stock
    total_articles = Stock.objects.aggregate(count=Count("id"))
    # Compter les produits dont la quantité est inférieure ou égale au reorder_level(seuil d'alert)
    articles_critique = Stock.objects.filter(quantite__lte=F('seuil_alert')).count()
    # Top 7 des produits les plus vendus
    most_sold = SaleHistory.objects.values('designation').annotate(total_quantity=Sum('quantite_vendu')).order_by("-total_quantity")[:10]

    # Récupérer les ventes et calculer la somme par jours de la semaine
    #ventes_par_jour = SaleHistory.objects.annotate(jour_semaine=ExtractWeekDay('date_mise_a_jour')).values('jour_semaine').annotate(total_ventes=Sum(F('prix_unitaire') * F('quantite_vendu'))).order_by('jour_semaine')

    # Récupérer la date du début de la semaine
    debut_semaine = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
    # Récupérer les données groupées par jour de la semaine pour la semaine en cours
    ventes_semaine_en_cours = SaleHistory.objects.filter(date_mise_a_jour__gte=debut_semaine)\
        .annotate(day_of_week=Coalesce(ExtractWeekDay('date_mise_a_jour'), 7))\
        .values('day_of_week')\
        .annotate(total_ventes=Sum(F('prix_unitaire') * F('quantite_vendu')))\
        .order_by('day_of_week')

    # Récupérer les données groupées par jour de la semaine pour la semaine précédente
    debut_semaine_precedente = debut_semaine - timedelta(weeks=1)
    ventes_semaine_precedente = SaleHistory.objects.filter(date_mise_a_jour__range=[debut_semaine_precedente, debut_semaine - timedelta(days=0)])\
        .annotate(day_of_week=Coalesce(ExtractWeekDay('date_mise_a_jour'), 7))\
        .values('day_of_week')\
        .annotate(total_ventes=Sum(F('prix_unitaire') * F('quantite_vendu')))\
        .order_by('day_of_week')

    # Préparer les données pour le graphique
    #jours_semaine = ['Jour 1', 'Jour 2', 'Jour 3', 'Jour 4', 'Jour 5', 'Jour 6', 'Jour 7']
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    ventes_data = [0] * 7  # Initialiser avec des zéros pour chaque jour de la semaine

    for vente in ventes_semaine_en_cours:
        day_of_week = vente['day_of_week'] - 1  # Les jours de la semaine commencent à 1 dans Django, nous les ajustons pour commencer à 0
        total_ventes = vente['total_ventes']
        ventes_data[day_of_week - 1] += total_ventes

    ventes_data_2 = [0] * 7  # Initialiser avec des zéros pour chaque jour de la semaine
    for vente in ventes_semaine_precedente:
        day_of_week = vente['day_of_week'] - 1 # Les jours de la semaine commencent à 1 dans Django, nous les ajustons pour commencer à 0
        total_ventes = vente['total_ventes']
        ventes_data_2[day_of_week - 1] += total_ventes

    print(ventes_data)
    print()
    print(ventes_data_2)
    print(debut_semaine)
    print(debut_semaine_precedente)
    

    
    # Context Dictionary
    context = {
        "total_sale": total_sale,
        "total_supply": total_supply,
        "total_articles": total_articles,
        "articles_critique": articles_critique,
        'stock': most_sold,
        'jours_semaine': jours_semaine,
        'ventes_data': ventes_data,
        'ventes_data_2': ventes_data_2,
        'ventes_semaine_en_cours': ventes_semaine_en_cours,
        'ventes_semaine_precedente': ventes_semaine_precedente,
        'addForm': StockCreateForm(request.POST or None),
        'addSupplierForm': SupplierCreateUpdateForm(request.POST or None)
    }

    return render(request, 'core/index.html', context)

# =================================================== ADD NEW ITEM/Supplier ================================================

addItem
create_supplier

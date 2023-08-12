import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import DeleteView
from django.urls import reverse_lazy

from products.models import Categorie, Stock, SaleHistory, SupplyHistory
from products.forms import (
    StockCreateForm,
    StockUpdateForm,
    SearchItemForm,
    IssueForm,
    ReceiveForm,
    ReorderLevelForm,
    UpdateQuantityForm,
)


# ===================================================== STOCK LISTINGS ========================================================= #
def stock(request):
    stock = Stock.objects.all()
    template_name = 'products/stock/stock.html'

    page = request.GET.get('page', 1)

    paginator = Paginator(stock, 20)
    try:
        stock = paginator.page(page)
    except PageNotAnInteger:
        stock = paginator.page(1)
    except EmptyPage:
        stock = paginator.page(paginator.num_pages)

    form = SearchItemForm(request.POST or None)
    addForm = StockCreateForm(request.POST or None)


    if request.method == 'POST':
        categorie = form['categorie'].value()
        start_date = form['start_date'].value()
        end_date = form['end_date'].value()

        stock = Stock.objects.filter(
            designation__icontains=form['designation'].value(),
            #date_creation__range=[form['start_date'].value(), form['end_date'].value()]
        )

        if (categorie != ''):
            stock = stock.filter(categorie=categorie)

        if start_date and end_date:
            stock = stock.filter(date_creation__range=[start_date, end_date])
            
        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachement; filename="Liste des items {timezone.now()}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Référence', 'Désignation', 'Categorie', 'Quantité', 'prix_vente', 'seuil_alert'])
            instance = stock
            for s in instance:
                writer.writerow([s.reference, s.designation, s.categorie, s.quantite, s.prix_vente, s.seuil_alert])
            return response

    context = {
        'stock': stock,
        'form': form,
        'addForm': addForm,
        }
    return render(request, template_name, context)


# ================================================== EXPORT STOCK LIST IN CSV =================================================== #
def export_stock_to_csv(request):
    stock = Stock.objects.all() # fetch all objects in Stock model

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachement; filename="Liste des items {timezone.now()}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Référence', 'Désignation', 'Categorie', 'Quantité', 'prix_vente', 'seuil_alert'])
    instance = stock
    for s in instance:
        writer.writerow([s.reference, s.designation, s.categorie, s.quantite, s.prix_vente, s.seuil_alert])
    return response 


# ================================================== ADD NEW ITEM | Modal =================================================== #
@login_required(redirect_field_name='next', login_url='/accounts/login')
def addItem(request):
    addForm = StockCreateForm(request.POST or None)
    if request.method == 'POST':
        if addForm.is_valid():
            addForm.save()

            messages.success(request, "Item ajouté avec succès")
            return redirect('stock')
        else:
            messages.error(
            request, "Oopps!! Quelque chose s'est mal passé. Veillez réprendre!")
            return redirect('stock')
        
    return addForm
    


# ===================================================== ADD NEW ITEM ========================================================= #
@login_required(redirect_field_name='next', login_url='/accounts/login')
def add_item(request):
    template_name = 'products/add_item.html'

    form = StockCreateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.reference = form.cleaned_data['reference']
            instance.categorie = form.cleaned_data['categorie']
            instance.designation = form.cleaned_data['designation']
            instance.prix_achat = form.cleaned_data['prix_achat']
            instance.save()

            messages.success(request, "Item ajouté avec succès")
            return redirect('add_item')
        else:
            messages.error(
                request, "Oopps!! Quelque chose s'est mal passé. Veillez réprendre!")
            return redirect('add_item')

    context = {'form': form}

    return render(request, template_name, context)


# ===================================================== UPDATE ITEM ========================================================= #
@login_required(redirect_field_name='next', login_url='/accounts/login')
def update_item(request, pk):
    template_name = 'products/update_item.html'
    item = get_object_or_404(Stock, id=pk)
    
    form = StockUpdateForm(instance=item)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Mise à jour effectuée avec succès!")
            return redirect('stock')

    context = {
        'item': item,
        'form': form
    }

    return render(request, template_name, context)


# ===================================================== DELETE ITEM ========================================================= #
@login_required(redirect_field_name='next', login_url='/accounts/login')
def delete_item(request, pk):
    template_name = 'products/delete_item.html'
    item = get_object_or_404(Stock, id=pk)

    if request.method == 'POST':
        item.delete()
        messages.error(request, f"{item.designation} a été supprimé")
        return redirect('stock')
    return render(request, template_name, {'item': item})



class DeleteItem(DeleteView):
    model = Stock
    success_url = reverse_lazy('stock')



# ===================================================== ITEM DETAILS ========================================================= #
@login_required(redirect_field_name='next', login_url='/accounts/login')
def details_item(request, pk):
    template_name = 'products/details_item.html'
    item = get_object_or_404(Stock, id=pk)

    total_price = item.prix_vente * item.quantite
    issueForm = IssueForm(request.POST or None, instance=item)
    receiveForm = ReceiveForm(request.POST or None, instance=item)

    context = {
        'item': item,
        'total_price': total_price,
        'issueForm': issueForm,
        'receiveForm': receiveForm
    }

    return render(request, template_name, context)


# ===================================================== ISSUE ITEMS ========================================================= #
@login_required(redirect_field_name='next', login_url='/accounts/login')
def issue_items(request, pk):
    item = Stock.objects.get(id=pk)
    issueForm = IssueForm(request.POST or None, instance=item)
    if issueForm.is_valid():
        instance = issueForm.save(commit=False)
        # instance.delivre_a = str(request.user)
        # Si la quantité est inferière ou égale à 0, la soustraction est peut être faite. Pas de quantite (-)
        if instance.quantite <= 0:
            messages.error(request, "Erreur d'opération: La quantité ne peut être soustrait !")
        # Si la quantite démandée est superière à la quantité présente en stock, l'opération ne doit être accepter.
        if instance.quantite < instance.delivre_quantite:
            messages.error(request, "Erreur d'opération: La quantité à soustraire est superière à la quantite présente de l'item !")
        if instance.delivre_quantite <= 0:
            messages.error(request, "Error! La quantité à délivrer doit être superieure à Zéro")
        # Sinon procéder à l'opération
        else:
            instance.quantite -= instance.delivre_quantite
            instance.save()
            messages.success(
                request, "Délivré avec succès. " +
                str(instance.quantite) +
                " " + str(instance.designation) +
                "restant dans le stock"
            )
            # Générer la table de repport
            issue_history = SaleHistory(
                reference=instance.reference,
                designation=instance.designation,
                categorie=instance.categorie,
                quantite=instance.quantite,
                prix_unitaire=instance.prix_vente,
                quantite_vendu=instance.delivre_quantite,
                delivre_par=instance.delivre_par,
                delivre_a=instance.delivre_a,
                date_creation=instance.date_creation,
                date_mise_a_jour=instance.date_mise_a_jour,
            )
            issue_history.save()

        
        return redirect('/products/details_item/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    issueForm.reset()

    context = {
        "title": 'Délivrer ' + str(item.designation),
        "item": item,
        "issueForm": issueForm,
        "username": 'Délivré par : ' + str(request.user),
    }

    return context


# ===================================================== RECIEVE ITEMS ========================================================= #
@login_required(redirect_field_name='next', login_url='/accounts/login/')
def receive_items(request, pk):
    item = Stock.objects.get(id=pk)
    receiveForm = ReceiveForm(request.POST or None, instance=item)
    if receiveForm.is_valid():
        instance = receiveForm.save(commit=False)
        instance.quantite += instance.recevoir_quantite
        instance.save()

        receive_history = SupplyHistory(
            reference=instance.reference,
            designation=instance.designation,
            categorie_id=instance.categorie_id,
            quantite=instance.quantite,
            prix_unitaire=instance.prix_achat,
            quantite_recu=instance.recevoir_quantite,
            provient_de=instance.recu_par,
            date_creation=instance.date_creation,
            date_mise_a_jour=instance.date_mise_a_jour,
        )
        receive_history.save()

        messages.success(request, "Réçu avec succès. " + str(instance.quantite) +
                         " " + str(instance.designation)+" restant dans le Stock")

        return redirect('/products/details_item/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    
    receiveForm.reset()
    context = {
        "title": 'Récevoir ' + str(item.designation),
        "instance": item,
        "receiveForm": receiveForm,
        "username": 'Réçu par: ' + str(request.user),
    }

    return context


# ===================================================== RE-ORDER LEVEL ========================================================= #
@login_required(redirect_field_name='next', login_url='/accounts/login/')
def reorder_level(request, pk):
    item = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=item)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Le seuil d'alert pour " + str(
            instance.designation) + " a été mise à jour à " + str(instance.seuil_alert))

        return redirect("/products/stock/")
    context = {
        "item": item,
        "form": form,
    }
    return render(request, "products/reorder_level_item.html", context)


# ===================================================== Update Quantite ========================================================= #
@login_required
def update_quantity(request, pk):
    item = get_object_or_404(Stock, id=pk)

    form = UpdateQuantityForm(request.POST or None, instance=item)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, f"La quantité de {instance.designation} a été mise à jours à {instance.quantite}")
    
        return redirect("/products/stock/")
    
    context = {
        "item": item,
        "form": form,
    }

    return render(request, "products/update_quantity.html", context)


# ===================================================== SALE HISTORY ========================================================= #
@login_required(redirect_field_name='next', login_url='/accounts/login/')
def sale_history(request):
    queryset = SaleHistory.objects.all().order_by('-date_mise_a_jour')
    template_name = 'products/repport/sale_repport.html'
    header = "Historique Ventes"

    # PAGINATION
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    form = SearchItemForm(request.POST or None)

    # SEARCH
    if request.method == 'POST':
        categorie = form['categorie'].value()
        start_date = form['start_date'].value()
        end_date = form['end_date'].value()

        queryset = SaleHistory.objects.filter(
            #reference__icontains=form['reference'].value(),
            designation__icontains=form['designation'].value(),
            #date_creation__range=[form['start_date'].value(), form['end_date'].value()]
        )

        if (categorie != ''):
            queryset = queryset.filter(categorie=categorie)

        if start_date and end_date:
            queryset = queryset.filter(date_mise_a_jour__range=[start_date, end_date])

        # Export to CSV
        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachement; filename="Historique des Ventes {timezone.now()}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Référence', 'Categorie', 'Designation', 'Quantité En Stock', 'Quantité Délivrée', 'Date'])
            instance = queryset
            for s in instance:
                writer.writerow([s.reference, s.categorie, s.designation, s.quantite, s.quantite_vendu, s.date_mise_a_jour])
            return response

    # Context Dictionary
    context = {
        'header': header,
        'queryset': queryset,
        'form': form,
    }
    return render(request, template_name, context)


# ===================================================== SALE HISTORY ========================================================= #
@login_required(redirect_field_name='next', login_url='/accounts/login/')
def supply_history(request):
    queryset = SupplyHistory.objects.all().order_by('-date_mise_a_jour')
    template_name = 'products/repport/supply_repport.html'
    header = "Historique D'approvisionnement"

    # PAGINATION
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    form = SearchItemForm(request.POST or None)

    # SEARCH
    if request.method == 'POST':
        categorie = form['categorie'].value()
        start_date = form['start_date'].value()
        end_date = form['end_date'].value()

        queryset = SupplyHistory.objects.filter(
            #reference__icontains=form['reference'].value(),
            designation__icontains=form['designation'].value(),
            #date_creation__range=[form['start_date'].value(), form['end_date'].value()]
        )

        if (categorie != ''):
            queryset = queryset.filter(categorie=categorie)

        if start_date and end_date:
            queryset = queryset.filter(date_mise_a_jour__range=[start_date, end_date])

        # Export to CSV
        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachement; filename="Historique des Approvisionnements {timezone.now()}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Référence', 'Categorie', 'Designation', 'Quantité En Stock', 'Quantité Délivrée', 'Date'])
            instance = queryset
            for s in instance:
                writer.writerow([s.reference, s.categorie, s.designation, s.quantite, s.quantite_recu, s.date_mise_a_jour])
            return response

    # Context Dictionary
    context = {
        'header': header,
        'queryset': queryset,
        'form': form,
    }
    return render(request, template_name, context)
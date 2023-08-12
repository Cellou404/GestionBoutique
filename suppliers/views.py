import csv
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from suppliers.models import Suppliers
from suppliers.forms import SupplierCreateUpdateForm


def suppliers(request):
    suppliers = Suppliers.objects.all().order_by('-date_created')
    addSupplierForm = SupplierCreateUpdateForm(request.POST or None)

    page = request.GET.get('page', 1)

    paginator = Paginator(suppliers, 15)
    try:
        suppliers = paginator.page(page)
    except PageNotAnInteger:
        suppliers = paginator.page(1)
    except EmptyPage:
        suppliers = paginator.page(paginator.num_pages)

    query = request.GET.get('q')
    if query:
        suppliers = Suppliers.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(address__icontains=query) |
            Q(phone__iexact=query)|
            Q(town__icontains=query)
        ).distinct()

    context = {
        'suppliers': suppliers,
        'addSupplierForm': addSupplierForm
    }
    return render(request, "suppliers/suppliers.html", context)


def create_supplier(request):

    addSupplierForm = SupplierCreateUpdateForm(request.POST or None)
    if request.method == 'POST':
        if addSupplierForm.is_valid():
            addSupplierForm.save()
            messages.success(request, "Nouveau fournisseur ajouté avec succès!")
            return redirect('suppliers')
        else:
            messages.error(request, 'Error: Quelque chose s\'est mal passé lors de la soumission du formulaire')
            return redirect('suppliers')
        
    context = {
        'addSupplierForm': addSupplierForm,
    }

    return context

def update_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, id=pk)
    updateForm = SupplierCreateUpdateForm(request.POST or None, instance=supplier)

    if updateForm.is_valid():
        updateForm.save()
        messages.success(request, "Les informations du fournisseur ont bien été modifiés")
        return redirect("suppliers")
    
    context = {
        'supplier': supplier,
        'updateForm': updateForm
    }

    return render(request, template_name='suppliers/update_supplier.html', context=context)


def delete_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, id=pk)
    supplier.delete()
    messages.info(request, 'Le client a été suprimé de la liste avec succèss')

    return redirect('suppliers')



def export_to_csv(request):
    suppliers = Suppliers.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'ttachement; filename="Liste des fournisseurs_{timezone.now()}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Email', 'Addresse', 'Téléphone', 'Ville', 'Date Ajout'])
    instance = suppliers
    for i in instance:
        writer.writerow([i.name, i.email, i.address, i.phone, i.town, i.date_created])
    return response


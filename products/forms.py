from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from products.models import Stock


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reference', 'categorie', 'designation', 'prix_achat', 'pourcentage']

    def clean_reference(self):
          reference = self.cleaned_data['reference']
          if not reference:
                raise forms.ValidationError("Ce champ est réquit. Veillez le renseigner!")
          return reference
    
    def clean_categorie(self):
          categorie = self.cleaned_data.get('categorie')
          if (categorie == ""):
                raise forms.ValidationError("Ce champ est réquit. Veillez le renseigner!")
          return categorie
    
    def clean_designation(self):
          cleaned_data = super().clean()
          designation = cleaned_data['designation']
          if (designation == ""):
                raise forms.ValidationError("Ce champ est réquit. Veillez le renseigner!")
        
          for instance in Stock.objects.all():
                if instance.designation == designation:
                      raise forms.ValidationError(f"{designation} avait déjà été créé")
          return designation
          
    
    def clean_prix_achat(self):
          prix_achat = self.cleaned_data.get('prix_achat')
          if (prix_achat == ""):
                raise forms.ValidationError("Ce champ est réquit. Veillez le renseigner!")
          return prix_achat
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_show_labels = False 
        #self.helper.add_input(Submit('submit', 'Chercher', css_class='btn app-btn-primary'))

        self.helper.layout = Layout(
            Column('reference', css_class='form-group my-0'),
            Column('designation', css_class='form-group my-0'),
            Column('categorie', css_class='form-group my-0'),
            Row(
              Column('prix_achat', css_class='form-group col-md-6 mb-0'),
              Column('pourcentage', css_class='form-group col-md-6 mb-0'),
              css_class='form-row'
            ),
        )
    

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reference', 'categorie', 'designation']


class SearchItemForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['categorie','designation','start_date','end_date']

    reference = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Réference. Ex: REF03', 'class': 'form-control form-control-sm'}), required=False)
    designation = forms.CharField(label='Désignation', widget=forms.TextInput(attrs={'placeholder': 'Ex: Samsung A20', 'class': 'form-control form-control-sm'}), required=False)
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),required=False)
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),required=False)
    export_to_csv = forms.BooleanField(required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_show_labels = False 
        #self.helper.add_input(Submit('submit', 'Chercher', css_class='btn app-btn-primary'))

        self.helper.layout = Layout(
            Row(
              Column('categorie', css_class='form-group col-md-6 mb-0'),
              Column('designation', css_class='form-group col-md-6 mb-0'),
              css_class='form-row'
            ),
            Row(
                Column('start_date', css_class='form-group col-md-6 mb-0'),
                Column('end_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('export_to_csv', css_class='form-group col-md-6 mb-0'),
                Column(Submit('submit', 'Chercher', css_class='form-group col-md-6 mb-0 btn app-btn-primary py-1 w-100')),
                css_class='form-row'
            )
        )


class IssueForm(forms.ModelForm):
      delivre_a = forms.CharField(label='Délivrer à',required=True, help_text='Destinataire')      
      class Meta:
            model = Stock
            fields = ['delivre_quantite', 'delivre_a']


class ReceiveForm(forms.ModelForm):
      recu_par = forms.CharField(label='Source',required=True)
      class Meta:
            model = Stock
            fields = ['recevoir_quantite', 'recu_par']
                

class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['seuil_alert']
                

class UpdateQuantityForm(forms.ModelForm):
      class Meta:
            model = Stock
            fields = ['quantite']




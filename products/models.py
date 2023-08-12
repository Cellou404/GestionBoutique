from django.db import models
from django.utils.translation import gettext_lazy as _


class Categorie(models.Model):
    nom = models.CharField(_('Nom'), max_length=100)

    class Meta:
        verbose_name = _('Categorie')
        verbose_name_plural = _('Categories')


    def __str__(self):
        return self.nom


class Stock(models.Model):
    reference = models.CharField(_('Référence'), max_length=50, blank=True, null=True)
    designation = models.CharField(_('Désignation'), max_length=150, help_text=_("Nom de l'item"), blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, blank=True, null=True)
    quantite = models.IntegerField(_('Quantité'), default=0, blank=True, null=True)
    prix_achat = models.PositiveIntegerField(_("Prix d'achat"), default=0, null=True, blank=True)
    prix_vente = models.IntegerField(_("Prix de vente"), default=0)
    pourcentage = models.PositiveIntegerField(_("Pourcentage"), default=0, null=True, blank=True)
    seuil_alert = models.IntegerField(_('Seuil d\'alert'), default=0, blank=True, null=True)

    recevoir_quantite= models.IntegerField(_('Récevoir une quantité'), default=0, blank=True, null=True)
    recu_par = models.CharField(_('Réçu par'), max_length=150, blank=True, null=True)
    delivre_quantite= models.IntegerField(_('Délivrer une quantité'), default=0, blank=True, null=True)
    delivre_par = models.CharField(_('Délivré par'), max_length=150, blank=True, null=True)
    delivre_a = models.CharField(_('Délivré à'), max_length=150, blank=True, null=True)
    
    date_creation = models.DateTimeField(_('Date de création'), auto_now_add=True, auto_now=False)
    date_mise_a_jour = models.DateTimeField(_('Date de mise à jour'),auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
        ordering = ['-date_creation']

    def __str__(self):
        return self.reference
    
    
    def save(self, *args, **kwargs):
        self.prix_vente = self.prix_achat + (self.prix_achat * self.pourcentage/100)

        super(Stock, self).save(*args, **kwargs)


    def get_total_price(self):
        return self.prix_vente * self.quantite

        

class SaleHistory(models.Model):
    reference = models.CharField(_('Référence'), max_length=50, blank=True, null=True)
    designation = models.CharField(_('Désignation'), max_length=150, help_text=_("Nom de l'item"))
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, blank=True, null=True)
    quantite = models.IntegerField(_('Quantité'), default=0, blank=True, null=True)
    prix_unitaire = models.IntegerField(_("Prix unitaire"), default=0, blank=True, null=True)
    
    quantite_vendu= models.IntegerField(_('Quantité délivrée'), default=0, blank=True, null=True)
    delivre_par = models.CharField(_('Délivré par'), max_length=150, blank=True, null=True)
    delivre_a = models.CharField(_('Délivré à'), max_length=150, blank=True, null=True)
    
    date_creation = models.DateTimeField(_('Date de création'), auto_now_add=False, auto_now=False, null=True)
    date_mise_a_jour = models.DateTimeField(_('Date de mise à jour'),auto_now_add=False, auto_now=False, null=True)

    class Meta:
        verbose_name = _('Historique Vente')
        verbose_name_plural = _('Historique Ventes')
        ordering = ['-date_mise_a_jour']

    def __str__(self):
        return self.reference
    
    def get_total_price(self):
        return self.prix_unitaire * self.quantite_vendu
    

class SupplyHistory(models.Model):
    reference = models.CharField(_('Référence'), max_length=50, blank=True, null=True)
    designation = models.CharField(_('Désignation'), max_length=150, help_text=_("Nom de l'item"))
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, blank=True, null=True)
    quantite = models.IntegerField(_('Quantité'), default=0, blank=True, null=True)
    prix_unitaire = models.IntegerField(_("Prix unitaire"), default=0, blank=True, null=True)

    quantite_recu= models.IntegerField(_('Quantité réçu'), default=0, blank=True, null=True)
    provient_de = models.CharField(_('Provient de'), max_length=150, blank=True, null=True)
    
    date_creation = models.DateTimeField(_('Date de création'), auto_now_add=False, auto_now=False, null=True)
    date_mise_a_jour = models.DateTimeField(_('Date de mise à jour'),auto_now_add=False, auto_now=False, null=True)

    class Meta:
        verbose_name = _('Historique D\'approvisionnement ')
        verbose_name_plural = _('Historique D\'approvisionnements')
        ordering = ['-date_mise_a_jour']

    def __str__(self):
        return self.reference
    
    def get_total_price(self):
        return self.prix_unitaire * self.quantite_recu

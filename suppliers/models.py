from django.db import models
from django.utils.translation import gettext as _


class Suppliers(models.Model):
    name = models.CharField(_("Nom"), max_length=150, blank=True, null=True)
    email = models.CharField(_("email"), max_length=100, blank=True, null=True)
    address = models.CharField(_("address"), max_length=100, blank=True, null=True)
    phone = models.CharField(_("téléphone"), max_length=50, blank=True, null=True)
    town = models.CharField(_("ville"), max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(_("Date"), auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Fournisseur")
        verbose_name_plural = _("Fournisseurs")

    def __str__(self):
        return self.name
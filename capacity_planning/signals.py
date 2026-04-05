# capacity_planning/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import ExternalCapacity, Supplier
from accounts.models import Department

@receiver(post_save, sender=ExternalCapacity)
def update_supplier_budgeted_hours_on_save(sender, instance, **kwargs):
    """Update Supplier's budgeted_hours when ExternalCapacity is added or updated"""
    instance.supplier.update_budgeted_hours()


@receiver(post_delete, sender=ExternalCapacity)
def update_supplier_budgeted_hours_on_delete(sender, instance, **kwargs):
    """Update Supplier's budgeted_hours when ExternalCapacity is deleted"""
    instance.supplier.update_budgeted_hours()
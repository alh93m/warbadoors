"""Atomic inventory helpers — use from views/signals; never duplicate stock math in templates."""

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from inventory.models import ColorStock
from reservations.models import Reservation


@transaction.atomic
def apply_reservation_approval(
    reservation_id: int,
    *,
    approved_by_id=None,
    min_available: int = 0,
) -> Reservation:
    """
    Approve a reservation and increment reserved_quantity under row lock.

    Raises ValueError if stock is insufficient. Caller must enforce auth/roles.
    """
    reservation = (
        Reservation.objects.select_for_update()
        .select_related('color')
        .get(pk=reservation_id)
    )
    if reservation.status != 'pending':
        raise ValueError('Only pending reservations can be approved.')

    stock = (
        ColorStock.objects.select_for_update()
        .select_related('color')
        .get(color_id=reservation.color_id)
    )

    available = stock.total_quantity - stock.reserved_quantity - stock.damaged_quantity
    if available - reservation.quantity < min_available:
        raise ValueError('Insufficient available stock for this reservation.')

    ColorStock.objects.filter(pk=stock.pk).update(
        reserved_quantity=F('reserved_quantity') + reservation.quantity
    )
    stock.refresh_from_db(
        fields=['reserved_quantity', 'total_quantity', 'damaged_quantity']
    )
    stock.calculate_available()
    stock.save(update_fields=['available_quantity', 'needs_reorder', 'last_updated'])

    reservation.status = 'approved'
    reservation.approved_at = timezone.now()
    update_fields = ['status', 'approved_at', 'updated_at']
    if approved_by_id is not None:
        reservation.approved_by_id = approved_by_id
        update_fields.append('approved_by')
    reservation.save(update_fields=update_fields)
    return reservation


@transaction.atomic
def release_reservation_stock(reservation_id: int) -> tuple[Reservation, int]:
    """
    Decrement reserved_quantity for an approved reservation (e.g. reject/cancel after approval).

    Returns (reservation, units_released). Caller should persist reservation status.
    """
    reservation = (
        Reservation.objects.select_for_update()
        .select_related('color')
        .get(pk=reservation_id)
    )
    if reservation.status != 'approved':
        raise ValueError('Stock can only be released for approved reservations.')

    stock = ColorStock.objects.select_for_update().get(color_id=reservation.color_id)
    decrement = min(reservation.quantity, stock.reserved_quantity)
    ColorStock.objects.filter(pk=stock.pk).update(
        reserved_quantity=F('reserved_quantity') - decrement
    )
    stock.refresh_from_db(
        fields=['reserved_quantity', 'total_quantity', 'damaged_quantity']
    )
    stock.calculate_available()
    stock.save(update_fields=['available_quantity', 'needs_reorder', 'last_updated'])
    return reservation, decrement

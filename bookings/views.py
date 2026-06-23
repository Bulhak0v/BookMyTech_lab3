from rest_framework import viewsets, permissions
from .models import Booking, Notification
from .serializers import BookingSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import BookingWebForm
from inventory.models import Equipment



@login_required
def create_booking_web(request, item_id):
    equipment = get_object_or_404(Equipment, id=item_id)

    if request.method == 'POST':
        form = BookingWebForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.equipment = equipment

            conflicts = Booking.objects.filter(
                equipment=equipment,
                status='confirmed',
                start_date__lt=booking.end_date,
                end_date__gt=booking.start_date
            )

            if conflicts.exists():
                messages.error(request, "На жаль, на ці дати техніка вже заброньована.")
            else:
                booking.status = 'confirmed'
                booking.save()
                messages.success(request, f"Ви успішно забронювали {equipment.name}!")
                return redirect('equipment_list')
    else:
        form = BookingWebForm()

    return render(request, 'booking_form.html', {
        'form': form,
        'equipment': equipment
    })


@login_required
def my_bookings_web(request):
    user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'my_bookings.html', {
        'bookings': user_bookings,
        'now': timezone.now()
    })


@login_required
def cancel_booking_web(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f"Бронювання {booking.equipment.name} скасовано.")
    else:
        messages.error(request, "Це бронювання не можна скасувати.")

    return redirect('my_bookings')

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user == instance.user or self.request.user.role == 'admin':
            instance.status = 'cancelled'
            instance.save()
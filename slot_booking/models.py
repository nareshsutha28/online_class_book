from django.db import models
from user.models import User


# Model for Teacher Availability Slot
class TeacherAvailabilitySlot(models.Model):
    
    teacher = models.ForeignKey(User, related_name="slots", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


# Model for Slot Booking
class SlotBooking(models.Model):
    student = models.ForeignKey(User, related_name="booked_slots", on_delete=models.CASCADE)
    slot = models.ForeignKey(TeacherAvailabilitySlot, related_name="bookings", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

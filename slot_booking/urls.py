from django.urls import path
from slot_booking.views import TeacherSlotAPIView, StudentTeacherSlotsAPIView


urlpatterns = [
    path('teacher-slots/', TeacherSlotAPIView.as_view(), name='teacher_slot_get_create'),
    path('teacher-available-slot/', StudentTeacherSlotsAPIView.as_view(), name='teacher_available_slot'),
]

from django.urls import path
from slot_booking.views import TeacherSlotAPIView


urlpatterns = [
    path('teacher-slots/', TeacherSlotAPIView.as_view(), name='teacher_slot_get_create'),
]

from django.urls import path
from slot_booking.views import TeacherSlotAPIView, StudentTeacherSlotsAPIView, BookSlotAPIView, DefaultSlotBookApiView


urlpatterns = [
    path('teacher-slots/', TeacherSlotAPIView.as_view(), name='teacher_slot_get_create'),
    path('teacher-available-slot/', StudentTeacherSlotsAPIView.as_view(), name='teacher_available_slot'),
    path('book-class-slot/', BookSlotAPIView.as_view(), name='book_class_slot'),
    path('set-default-class-slot/', DefaultSlotBookApiView.as_view(), name='set_default_class_slot'),
]

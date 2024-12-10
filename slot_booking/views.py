from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user.models import User
from slot_booking.models import TeacherAvailabilitySlot
from slot_booking.serializers import TeacherAvailabilitySlotSerializer, AvailableSlotForStudent
from online_class_book.utils import get_response
from rest_framework.pagination import PageNumberPagination
from django.utils.timezone import now
from datetime import datetime


class TeacherSlotAPIView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination  # Enable pagination for this view


    def get(self, request):
        """
        Retrieve all upcoming availability slots for the authenticated teacher.
        """
        # Filter future availability slots for the teacher and order by start_time
        slot_queryset = TeacherAvailabilitySlot.objects.filter(
            teacher=request.user,
            start_time__gt=now()  # Only include slots starting after the current time
        ).order_by('start_time')

        # Paginate the queryset
        slots = self.paginate_queryset(slot_queryset)

        # Serialize the paginated slots
        serializer = TeacherAvailabilitySlotSerializer(slots, many=True)

        # Return the paginated response with serialized data
        return self.get_paginated_response(serializer.data)


    def post(self, request):
        # Check if the user is a teacher
        if request.user.role != User.UserRole.TEACHER:
            return get_response(
                status.HTTP_403_FORBIDDEN,
                "You do not have permission to add slots.",
                {}
            )

        # Add the teacher ID to the request data
        data = request.data.copy()
        data["teacher"] = request.user.id

        # Serialize and validate the input data
        serializer = TeacherAvailabilitySlotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the slot with the logged-in teacher
            return get_response(status.HTTP_201_CREATED, "Your slot created successfully!", serializer.data)
        return get_response(status.HTTP_400_BAD_REQUEST, serializer.errors, {})


class StudentTeacherSlotsAPIView(GenericAPIView):
    """
    API for students to retrieve teacher slots with optional filters for subject and start_date.
    """
    pagination_class = PageNumberPagination  # Enable pagination for this view
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all teacher slots with optional filtering by subject and start_date.
        """
        # Get query parameters
        subject = request.query_params.get("subject", None)  # Filter by subject
        date = request.query_params.get("date", None)  # Filter by start_date

        # Filter teacher slots
        slots_queryset = TeacherAvailabilitySlot.objects.select_related('teacher').filter(
            start_time__gt=now()  # Only future slots
        )

        # Filter by subject if provided
        if subject:
            slots_queryset = slots_queryset.filter(teacher__teacher_profile__subject__icontains=subject)

        # Filter by start_date if provided
        if date:
            try: 
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except:
                return get_response(status.HTTP_400_BAD_REQUEST, "Please Pass Valid Date Params in 'YYYY-MM-DD' format", {})
        
            slots_queryset = slots_queryset.filter(start_time__date=date)

        # Order slots by start_time
        slots_queryset = slots_queryset.order_by('start_time')

        # Paginate the queryset
        slots = self.paginate_queryset(slots_queryset)

        # Serialize the paginated slots
        serializer = AvailableSlotForStudent(slots, many=True)

        # Return the paginated response with serialized data
        return self.get_paginated_response(serializer.data)

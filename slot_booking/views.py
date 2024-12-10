from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user.models import User
from slot_booking.models import TeacherAvailabilitySlot
from .serializers import TeacherAvailabilitySlotSerializer
from online_class_book.utils import get_response
from rest_framework.pagination import PageNumberPagination
from django.utils.timezone import now


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
        posts = self.paginate_queryset(slot_queryset)

        # Serialize the paginated slots
        serializer = TeacherAvailabilitySlotSerializer(posts, many=True)

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

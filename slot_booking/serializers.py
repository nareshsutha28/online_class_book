from rest_framework import serializers
from django.utils.timezone import now
from slot_booking.models import TeacherAvailabilitySlot
from user.serializers import UserSerializer


class TeacherAvailabilitySlotSerializer(serializers.ModelSerializer):
    # Define start_time and end_time with custom input and output formats
    start_time = serializers.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"],  # Input format
        format="%Y-%m-%d %H:%M"  # Output format
    )
    end_time = serializers.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"],  # Input format
        format="%Y-%m-%d %H:%M"  # Output format
    )
    reserved_students = serializers.SerializerMethodField()

    class Meta:
        model = TeacherAvailabilitySlot
        fields = ['id', 'teacher', 'start_time', 'end_time', 'reserved_students', 'created_at']
        read_only_fields = ['created_at']

    def validate_start_time_and_end_time(self, start_time, end_time):
        """Validate time logic between start_time and end_time."""
        if start_time >= end_time:
            raise serializers.ValidationError("Start time must be earlier than end time.")
        if start_time.minute != 0 or end_time.minute != 0:
            raise serializers.ValidationError("Time must be on the hour (e.g., 5:00, 10:00).")
        return start_time, end_time

    def validate_future_dates(self, start_time, end_time):
        """Validate that the provided times are in the future."""
        current_date = now().date()
        if start_time.date() <= current_date or end_time.date() <= current_date:
            raise serializers.ValidationError("Slots must be scheduled for future dates.")
        return start_time, end_time

    def validate_slot_overlap(self, teacher, start_time, end_time):
        """Check if the slot overlaps with existing slots for the same teacher."""
        if TeacherAvailabilitySlot.objects.filter(
            teacher=teacher,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists():
            raise serializers.ValidationError("This time slot overlaps with an existing slot.")

    def validate(self, data):
        """Consolidated validation for the serializer."""
        start_time = data['start_time']
        end_time = data['end_time']
        teacher = data['teacher']

        # Validate times and dates
        self.validate_start_time_and_end_time(start_time, end_time)
        self.validate_future_dates(start_time, end_time)
        self.validate_slot_overlap(teacher, start_time, end_time)

        return data

    def get_reserved_students(self, obj):
        booked_slots = obj.bookings.all()
        student_list = []
        for slot in booked_slots:
            student_list.append(UserSerializer(slot.student).data)

        return student_list


class AvailableSlotForStudent(serializers.ModelSerializer):
    
    # Define start_time and end_time with custom input and output formats
    start_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M"  # Output format
    )
    end_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M"  # Output format
    )
    teacher = UserSerializer(many=False)
    subject = serializers.CharField(source='teacher.teacher_profile.subject', read_only=True)

    class Meta:
        model = TeacherAvailabilitySlot
        fields = ['id', 'teacher', 'start_time', 'end_time', 'subject', 'created_at']
        read_only_fields = ['created_at']


class SlotBookingForStudentSerializer(serializers.ModelSerializer):

    slot = AvailableSlotForStudent(many=False)

    class Meta:
        model = TeacherAvailabilitySlot
        fields = ['id', 'slot', 'created_at']
        read_only_fields = ['created_at']

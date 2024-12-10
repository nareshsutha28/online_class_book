from rest_framework import serializers
from django.contrib.auth import authenticate
from user.models import User, TeacherProfile


class UserSerializer(serializers.ModelSerializer):
    
    # For Subject Field For Teacher
    subject = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'age', 'role', 'password', 'subject']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        # Create the user with the provided data
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data['age'],
            phone=validated_data['phone'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()

        if user.role == User.UserRole.TEACHER:
            TeacherProfile.objects.create(
                user = user,
                subject = validated_data['subject'] 
            )
        return user

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 10:  # Adjust length based on requirements
            raise serializers.ValidationError("Phone number must be exactly 10 digits long.")
        return value

    def validate(self, data):
        # Validation for Subject 
        if data.get("role") == User.UserRole.TEACHER:
            if not data.get("subject"):
                raise serializers.ValidationError("Missing Subject Details.")
        return data


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data

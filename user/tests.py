from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPITests(TestCase):
    def setUp(self):
        """
        Set up URLs and initial data for testing.
        """
        self.register_url = reverse("register")
        self.student_payload = {
            "email": "student@yopmail.com",
            "first_name": "Student",
            "last_name": "User",
            "phone": "8498364650",
            "age": 19,
            "role": "Student",
            "password": "Student@123"
        }
        self.teacher_payload = {
            "email": "teacher@yopmail.com",
            "first_name": "Teacher",
            "last_name": "User",
            "phone": "8498364650",
            "age": 25,
            "role": "Teacher",
            "password": "Teacher@123",
            "subject": "Math"
        }

    def test_create_student_user(self):
        """
        Test creating a student user and handling duplicate email and phone.
        """
        # Create the first student user
        response = self.client.post(self.register_url, self.student_payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("User registered successfully!", response.json()["msg"])

        # Try creating a user with the same email and phone
        response = self.client.post(self.register_url, self.student_payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.json()["msg"])  # Validate duplicate email error
        self.assertIn("phone", response.json()["msg"])  # Validate duplicate phone error
    
    def test_create_teacher_user(self):
        """
        Test creating a teacher user with and handling duplicate email and phone.
        """
        # Valid teacher registration
        response = self.client.post(self.register_url, self.teacher_payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("User registered successfully!", response.json()["msg"])

        # Try creating a user with the same email and phone
        response = self.client.post(self.register_url, self.teacher_payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.json()["msg"])  # Validate duplicate email error
        self.assertIn("phone", response.json()["msg"])  # Validate duplicate phone error


class LoginAPITests(TestCase):
    def setUp(self):
        """
        Set up URLs, test users, and their credentials.
        """
        self.login_url = reverse("login")
        
        # Test users
        self.user = User.objects.create_user(
            email="student@yopmail.com",
            first_name="Student",
            last_name="User",
            phone="8498364650",
            age=19,
            role="Student"
        )
        self.user.set_password("Student@123")
        self.user.save()


    def test_login_user(self):
        """
        Test logging in as user.
        """
        response = self.client.post(self.login_url, {
            "email": "student@yopmail.com",
            "password": "Student@123"
        }, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["data"]
        self.assertIn("access", data)  # Verify access token
        self.assertIn("refresh", data)  # Verify refresh token
        self.assertIn("user_details", data)

    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        response = self.client.post(self.login_url, {
            "email": "student@yopmail.com",
            "password": "WrongPassword"
        }, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.json()["msg"])  # Check for invalid credentials error


class RefreshTokenAPITests(TestCase):
    def setUp(self):
        """
        Set up URLs, test users, and their tokens.
        """
        self.refresh_url = reverse("refresh")
        
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@yopmail.com",
            first_name="Test",
            last_name="User",
            phone="8498364650",
            age=19,
            role="Student",
        )
        self.user.set_password("Test@123")
        self.user.save()

        # Generate valid tokens for the test user
        refresh = RefreshToken.for_user(self.user)
        self.valid_refresh_token = str(refresh)

    def test_valid_refresh_token(self):
        """
        Test refreshing an access token using a valid refresh token.
        """
        response = self.client.post(self.refresh_url, {
            "refresh": self.valid_refresh_token
        }, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json()["data"])  # Check if access token is in the response

    def test_missing_refresh_token(self):
        """
        Test refreshing an access token without providing a refresh token.
        """
        response = self.client.post(self.refresh_url, {}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("refresh", response.json())  # Check for missing token error

    def test_invalid_refresh_token(self):
        """
        Test refreshing an access token using an invalid refresh token.
        """
        response = self.client.post(self.refresh_url, {
            "refresh": "invalid_refresh_token"
        }, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Token is invalid or expired", str(response.json()["msg"]))


class LogoutAPITests(TestCase):
    def setUp(self):
        """
        Set up URLs, test users, and their tokens.
        """
        self.logout_url = reverse("logout")

        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@yopmail.com",
            first_name="Test",
            last_name="User",
            phone="8498364650",
            age=19,
            role="Student",
            password="Test@123"
        )

        # Generate valid tokens for the test user
        self.refresh = RefreshToken.for_user(self.user)
        self.valid_refresh_token = str(self.refresh)
        self.access_token = str(self.refresh.access_token)

    def test_successful_logout(self):
        """
        Test logging out with a valid refresh token.
        """
        response = self.client.post(self.logout_url, {
            "refresh": self.valid_refresh_token
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["msg"], "Logout successful")

    def test_invalid_refresh_token(self):
        """
        Test logging out with an invalid refresh token.
        """
        response = self.client.post(self.logout_url, {
            "refresh": "invalid_refresh_token"
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid or expired refresh token", response.json()["msg"])

    def test_logout_without_authentication(self):
        """
        Test logging out without authentication.
        """
        response = self.client.post(self.logout_url, {
            "refresh": self.valid_refresh_token
        }, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid Access key", str(response.content))

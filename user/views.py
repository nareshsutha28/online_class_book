from rest_framework.generics import GenericAPIView
from rest_framework import status
from online_class_book.utils import get_response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from user.serializers import UserSerializer, LoginUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class RegisterUserView(GenericAPIView):

    permission_classes = [AllowAny]

    """
    API endpoint to register a new user using GenericAPIView.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user and return success response
            serializer.save()
            return get_response(status.HTTP_201_CREATED, "User registered successfully!", {})

        return get_response(status.HTTP_400_BAD_REQUEST, serializer.errors, {})


class LoginAPIView(GenericAPIView):

    permission_classes = [AllowAny]

    """
    API to log In a user with email and password.
    """
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            user_serializer = UserSerializer(user)

            data = {
                    'refresh': refresh_token,
                    'access': access_token
                }
            data['user_details'] = user_serializer.data

            # Custom response
            return get_response(status.HTTP_200_OK, "Login successful !", data) 

        # Custom error response
        return get_response(status.HTTP_400_BAD_REQUEST, serializer.errors, {})


class CustomRefreshTokenView(GenericAPIView):

    permission_classes = [AllowAny]
    """
    API to refresh Access token.
    """
    def post(self, request):
        try:
            serializer = TokenRefreshSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # Get the new access token from the serializer
                access_token = serializer.validated_data.get('access')
                data = {
                        "access": access_token
                    }
                return get_response(status.HTTP_200_OK, "Token refreshed successfully", data)

        except (InvalidToken, TokenError) as e:
            # Handle invalid refresh token
            return get_response(status.HTTP_400_BAD_REQUEST, e.args, {})


class LogoutApiView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    """
    API to log out a user by blacklisting their refresh token.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return get_response(status.HTTP_400_BAD_REQUEST, "Refresh token is required", {})
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token
            return get_response(status.HTTP_200_OK, "Logout successful", {})

        except TokenError as e:
            return get_response(status.HTTP_400_BAD_REQUEST, "Invalid or expired refresh token", {})

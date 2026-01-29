# Create your views here.
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .seralizers import LoginSerializer, UserSerializer


@extend_schema(
    request=UserSerializer,
    responses={
        201: UserSerializer,
        400: UserSerializer,
    },
    description="Register a new user account",
    summary="User Registration",
    tags=["Users"],
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.
    POST /api/users/register/

    Request body:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User registered successfully", "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses={
        200: UserSerializer,
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        401: {"type": "object", "properties": {"error": {"type": "string"}}},
    },
    description="Login a user with email and password",
    summary="User Login",
    tags=["Users"],
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login a user with email and password.
    POST /api/users/login/

    Request body:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not check_password(password, user.password):
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    refresh = RefreshToken.for_user(user)
    serializer = UserSerializer(user)
    return Response(
        {
            "message": "Login successful",
            "user": serializer.data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout user by blacklisting the refresh token.
    """
    try:
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
        )
    except Exception:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        """Return queryset filtered to current user only."""
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def get_user(self, request):
        """
        Custom action to get the current authenticated user's profile.
        Endpoint: GET /api/users/get_user/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def update_user(self, request):
        """
        Custom action to update the current authenticated user's profile.
        Endpoint: POST /api/users/update_user/
        """
        user = request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def delete_user(self, request):
        """
        Custom action to update the current authenticated user's profile.
        Endpoint: POST /api/users/delete_user/
        """
        user = request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response(
            {"message": "User account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    # end def

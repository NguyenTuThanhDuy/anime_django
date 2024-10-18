from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample

from authentication.models import UserAccountInfo
from authentication.serializers import UserSerializer, UserAccountInfoSerializer, ErrorSerializer
# Create your views here.


@extend_schema(
    operation_id="user_login",
    summary="User Login",
    description="Login using username and password.",
    request=UserSerializer,  # Use serializer to document request body
    responses={
        200: UserSerializer,  # Success response returns UserAccount data
        400: ErrorSerializer
    },
    examples=[
        OpenApiExample(
            "Login Example",
            summary="Successful login",
            value={
                "username": "johndoe",
                "password": "mypassword123"
            }
        ),
    ]
)
@api_view(['POST'])
def login(request: Request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        # Check if the user with the given username exists
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Create a response object
            response = JsonResponse(
                {
                    'user_id': user.id,
                    'refresh_token': str(refresh),
                    'access_token': access_token,
                },
                status=status.HTTP_200_OK
            )

            # Set access token as an HTTP-only cookie
            response.set_cookie(
                key='access_token',
                value=access_token,
                max_age=300,         # Optional: lifespan of the cookie in seconds
                # path='/',             # Path where the cookie is valid
                # domain="localhost",          # Domain where the cookie is valid
                secure=False,         # Since using HTTP, ensure 'secure' is False
                httponly=False,       # If True, client-side JavaScript cannot access the cookie
                samesite='Lax',       # Controls cross-site request behavior ('Lax', 'Strict', 'None')
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=False,
                secure=False,  # Set to True in production (for HTTPS)
                samesite='Lax',
                max_age=3600,  # Token expiry in seconds
            )

            return response
        else:
            # If password is incorrect
            return Response({'msg': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        # If user with the given username does not exist
        return Response({'msg': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    operation_id="user_signup",
    summary="User Signup",
    description="Signup using username and password.",
    request=UserAccountInfoSerializer,  # Use serializer to document request body
    responses={
        200: UserAccountInfoSerializer,  # Success response returns UserAccount data
        400: ErrorSerializer
    },
    examples=[
        OpenApiExample(
            "Login Example",
            summary="Successful login",
            value={
                "user_account": {
                    "username": "duy@gmail.com",
                    "password": "Mot23Bon56!@"
                },
                "firstname": "John",
                "lastname": "Doe",
                "date_of_birth": "1990-01-01",
                "phone_number": "0913906655"
            }
        ),
    ]
)
@api_view(['POST'])
def signup(request):
    user_account = request.data.get('user_account')
    username = user_account.get('username')
    user = User.objects.filter(username=username).exists()
    if user:
        return Response({"msg": "Username is exist"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserAccountInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'User created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    operation_id="userinfo_modification",
    summary="UserInfo Modification",
    description="Modify user info by id.",
    request=UserAccountInfoSerializer,  # Use serializer to document request body
    responses={
        200: UserAccountInfoSerializer,  # Success response returns UserAccount data
        400: ErrorSerializer
    },
    examples=[
        OpenApiExample(
            "Modification Example",
            summary="Modify successfully",
            value={
                "firstname": "UpdatedFirstName",
                "lastname": "UpdatedLastName",
                "date_of_birth": "1991-02-02",
                "phone_number": "9876543210"
            }
        ),
    ]
)
@api_view(['PUT'])
def update_user_account_info(request, user_id: int):
    try:
        # Retrieve the specific UserAccountInfo record by the UserAccount id
        user_info = UserAccountInfo.objects.get(user_account_id=user_id)
    except UserAccountInfo.DoesNotExist:
        return Response({'msg': 'UserAccountInfo not found'}, status=status.HTTP_404_NOT_FOUND)

    # Use the serializer to update the UserAccountInfo
    serializer = UserAccountInfoSerializer(user_info, data=request.data,
                                           partial=True)  # partial=True allows partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'msg': 'UserAccountInfo updated successfully', 'data': serializer.data},
            status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from urllib import request
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response 
from rest_framework import status
from django.contrib.auth import get_user_model
from .utils import generate_access_token, generate_refresh_token
from .serializers import UserSerializer, DistricUserCreateSerializer
from .models import Token ,User 
from django.http import JsonResponse
# admin login

@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    User = get_user_model()
    response = Response()
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username, is_superuser=True).first()
    if(user is None):
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            "message": "invalid credentials",
            "status": status_code
        }
        return Response(response, status=status_code)
        
    if(not user.check_password(password)):
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            "message": "invalid credentials",
            "status": status_code
        }
        return Response(response, status=status_code)
    serializer_data = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    status_code = status.HTTP_200_OK
    response = {
        'message': "successfully logined",
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': serializer_data
    }
    return Response(response, status=status_code)


# district user login view
@api_view(['POST'])
@permission_classes([AllowAny])
def district_user_login(request):
    User = get_user_model()
    response = Response()
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username, is_district_user=True).first()
    if(user is None):
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            "message": "invalid credentials",
            "status": status_code
        }
        return Response(response, status=status_code)
        
    if(not user.check_password(password)):
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            "message": "invalid credentials",
            "status": status_code
        }
        return Response(response, status=status_code)
    serializer_data = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    status_code = status.HTTP_200_OK
    response = {
        'message': "successfully logined",
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': serializer_data
    }
    return Response(response, status=status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_district_user(request):
    serializer = DistricUserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_200_OK
        response = {
            "message":"district user created successfully",
            "data": serializer.data
        }
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            "message": "user creation failed",
            "data": serializer._errors
        }
    return Response(response, status=status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def userlogout(request):
    authorization_header = request.headers.get('Authorization')
    access_token = authorization_header.split(' ')[1]
    blacklisted = Token(blacklistedtoken = access_token)
    blacklisted.save()
    return Response("Token blacklisted Success")

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def userList(request):
    if request.method == 'GET':
        districts_name =list(User.objects.filter(is_district_user=True).values_list("username",flat=True))

        return Response( districts_name)
    elif request.method == 'POST':
        return Response( "POST method not allowed")

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def resetPassword(request):
    if request.method == 'POST':
        data= request.data
        username = data["username"]
        newpassword = data["newpassword"]
        user = User.objects.get(username=username)
        user.set_password(newpassword)
        user.save()
        response = {
            "message":"Password reset sucessfully",
        }
        return Response(response)
    elif request.method == 'GET':
        return Response( "GET method not allowed")

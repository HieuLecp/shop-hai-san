from .models import *
from .serializers import *
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics,filters

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import BasePermission
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import authentication_classes, permission_classes

import os
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import authenticate, login, logout

@swagger_auto_schema(
    method='get',
    operation_summary="Đăng xuất người dùng",
    operation_description="Đăng xuất tài khoản người dùng.",
    tags=['Xác thực']
)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'username': openapi.Schema(type=openapi.TYPE_STRING),
                            'password': openapi.Schema(type=openapi.TYPE_STRING),
                        },
                        required=['username', 'password'],
                    ),
    operation_summary="Đăng nhập người dùng",
    operation_description="Đăng nhập tài khoản người dùng.",
    tags=['Xác thực']
)
@api_view(['GET', 'POST'])
def User_authentication(request):
    if request.method == 'GET':
        logout(request)
        return Response({'message': 'Bạn đã đăng xuất thành công.'}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực thông tin đăng nhập
        user = authenticate(request, username=username, password=password)
        print('user:',user)
        if user is not None:
            # Đăng nhập thành công
            login(request, user)
            message = {'code':'200',
                   'message': 'Đăng nhập thành công',
                   'data': CustomerSerializer(user,context={'request': request}).data
                   }
            return Response(message, status=status.HTTP_200_OK)
        else:
            # Đăng nhập không thành công
            return Response({'error': 'Tên người dùng hoặc mật khẩu không đúng.'}, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(
    method='get',
    operation_summary="Duy trì đăng nhập người dùng",
    operation_description="Duy trì đăng nhập người dùng.",
    tags=['Xác thực']
)
@api_view(['GET'])
def Keep_login(request):
    user = request.user
    message = {'code':'200',
                   'message': 'Đăng nhập thành công',
                   'data': CustomerSerializer(user,context={'request': request}).data
                   }
    return Response(message, status=status.HTTP_200_OK)

# @swagger_auto_schema(method='post', request_body=CustomerSerializer)
@swagger_auto_schema(method='post',
                     operation_summary="Tạo tài khoản người dùng",
                     request_body=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'username': openapi.Schema(type=openapi.TYPE_STRING),
                            'password': openapi.Schema(type=openapi.TYPE_STRING),
                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                            'is_staff':openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        },
                        required=['username', 'password','email'],
                    ),
                    operation_description="API này được sử dụng để tạo tài khoản người dùng mới.",
                    tags=['Người dùng']
                    )
@swagger_auto_schema(
    method='get',
    operation_summary="Lấy danh sách tài khoản người dùng",
    operation_description="API này được sử dụng để lấy danh sách tất cả các tài khoản người dùng.",
    tags=['Người dùng']
)
@api_view(['GET', 'POST'])
def User_data(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ yêu cầu POST
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        is_staff = request.data.get('is_staff')

        # Kiểm tra các trường bắt buộc
        if not username or not password or not email:
            return Response({'error': 'Thiếu dữ liệu'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo tài khoản người dùng mới
        if is_staff:
            user = Customer.objects.create_user(username=username, password=password, email=email,is_staff=is_staff)
        else:
            user = Customer.objects.create_user(username=username, password=password, email=email)
        cart = Cart.objects.create()
        user.Cart_product = cart
        user.save()
        message = {'code':'201',
                   'message': 'Tạo tài khoản thành công',
                   'data': CustomerSerializer(user,context={'request': request}).data
                   }
        return Response(message,status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        # Lấy danh sách tất cả các tài khoản người dùng
        users = Customer.objects.all()
        message = {'code':'200',
                   'message': 'Lấy danh sách thành công',
                   'data': CustomerSerializer(users, many=True,context={'request': request}).data
                   }
        return Response(message,status=status.HTTP_200_OK)
    
@swagger_auto_schema(
    method='get',
    operation_summary="Lấy chi tiết tài khoản người dùng",
    operation_description="API này được sử dụng để lấy chi tiết tài khoản người dùng.",
    tags=['Người dùng']
)
@swagger_auto_schema(
    method='patch',
    operation_summary="Cập nhật tài khoản người dùng",
    operation_description="Cập nhật tài khoản người dùng.",
    tags=['Người dùng']
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Xóa tài khoản người dùng",
    operation_description="Xóa tài khoản người dùng.",
    tags=['Người dùng']
)
@api_view(['GET','PATCH','DELETE'])
def User_detail(request,pk):
    if request.method == 'GET':
        user = Customer.objects.get(pk=pk)
        message = {'code':'200',
                   'message': 'Lấy chi tiết tài khoản thành công',
                   'data': CustomerSerializer(user,context={'request': request}).data
                   }
        return Response(message,status=status.HTTP_200_OK)
    if request.method == 'PATCH':
        user = Customer.objects.get(pk=pk)
        message = {'code':'200',
                   'message': 'Lấy chi tiết tài khoản thành công',
                   'data': CustomerSerializer(user,context={'request': request}).data
                   }
        return Response(message,status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        user = Customer.objects.get(pk=pk)
        user.delete()
        message = {'code':'200',
                   'message': 'Xóa tài khoản thành công',
                   }
        return Response(message,status=status.HTTP_200_OK)
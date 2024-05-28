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
from rest_framework.parsers import MultiPartParser, FormParser

# @swagger_auto_schema(method='post', request_body=CustomerSerializer)
@swagger_auto_schema(
    method='post',
    operation_summary="Tạo  bản ghi",
    consumes=['multipart/form-data'],
    manual_parameters=[
        openapi.Parameter('Name', openapi.IN_FORM, type=openapi.TYPE_STRING,required=True),
        openapi.Parameter('Describe', openapi.IN_FORM, type=openapi.TYPE_STRING,required=True),
        openapi.Parameter('Category', openapi.IN_FORM, type=openapi.TYPE_STRING,required=True),
        openapi.Parameter('Price', openapi.IN_FORM, type=openapi.TYPE_STRING,required=True),
        # openapi.Parameter('List_image', openapi.IN_FORM, type=openapi.TYPE_FILE,required=True),
        openapi.Parameter('List_image', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_FILE, format="binary"), required=True)
    ],
    operation_description="API này được sử dụng để tạo bản ghi mới.",
    tags=['Hải sản']
)
@swagger_auto_schema(
    method='get',
    operation_summary="Lấy danh sách bản ghi",
    operation_description="API này được sử dụng để lấy danh sách tất cả các bản ghi",
    tags=['Hải sản']
)
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def Seafood_data(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_staff:
                # Lấy dữ liệu từ yêu cầu POST
                Name = request.data.get('Name')
                Describe = request.data.get('Describe')
                Category = request.data.get('Category')
                Price = request.data.get('Price')
                List_image = request.FILES.getlist('List_image')
                
                sf = SeaFood.objects.create(Name=Name,Describe=Describe,Category=Category,Price=Price)
                
                if sf and List_image:
                    for i in List_image:
                        Image_SeaFood.objects.create(Image=i,Belong_SeaFood=sf)
                    sf = SeaFood.objects.get(pk=sf.id)
            
                message = {'code':'201',
                        'message': 'Tạo bản ghi thành công',
                        'data': SeaFoodSerializer(sf,context={'request': request}).data
                        }
                return Response(message,status=status.HTTP_201_CREATED)
            else:
                message = {'code':'401',
                        'message': 'Bạn không có quyền thục hiện chức năng này',
                        }
                return Response(message,status=status.HTTP_401_UNAUTHORIZED)
        else:
            message = {'code':'401',
                        'message': 'Cần xác thực trước khi thực hiện chức năng này',
                        }
            return Response(message,status=status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'GET':
        # Lấy danh sách tất cả các tài khoản người dùng
        sfs = SeaFood.objects.all()
        message = {'code':'200',
                'message': 'Lấy danh sách bản ghi thành công',
                'data': SeaFoodSerializer(sfs,many=True,context={'request': request}).data
                }
        return Response(message,status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary="Lấy chi tiết",
    operation_description="API này được sử dụng để lấy chi tiết",
    tags=['Hải sản']
)
@swagger_auto_schema(
    method='patch',
    operation_summary="Cập nhật  bản ghi",
    consumes=['multipart/form-data'],
    manual_parameters=[
        openapi.Parameter('Name', openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter('Describe', openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter('Category', openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter('Price', openapi.IN_FORM, type=openapi.TYPE_STRING),
        # openapi.Parameter('List_image', openapi.IN_FORM, type=openapi.TYPE_FILE,required=True),
        openapi.Parameter('List_image', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_FILE, format="binary"))
    ],
    operation_description="API này được sử dụng để cập nhật bản ghi",
    tags=['Hải sản']
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Xóa bản ghi",
    operation_description="API này được sử dụng Xóa bản ghi",
    tags=['Hải sản']
)
@api_view(['GET','PATCH','DELETE'])
@parser_classes([MultiPartParser, FormParser])
def Seafood_detail(request,pk):
    if request.method == 'GET':
        sf = SeaFood.objects.get(pk=pk)
        message = {'code':'200',
                   'message': 'Lấy chi tiết bản ghi thành công',
                   'data': SeaFoodSerializer(sf,context={'request': request}).data
                   }
        return Response(message,status=status.HTTP_200_OK)
    if request.method == 'PATCH':
        if request.user.is_authenticated:
            if request.user.is_staff:
                # Lấy dữ liệu từ yêu cầu POST
                Name = request.data.get('Name')
                Describe = request.data.get('Describe')
                Category = request.data.get('Category')
                Price = request.data.get('Price')
                List_image = request.FILES.getlist('List_image')
                
                sf = SeaFood.objects.get(pk=pk)
                if List_image:
                    img = Image_SeaFood.objects.filter(Belong_SeaFood=sf)
                    img.delete()
                    for i in List_image:
                        Image_SeaFood.objects.create(Image=i,Belong_SeaFood=sf)
                    sf = SeaFood.objects.get(pk=sf.id)
                if Name:
                    sf.Name=Name
                if Describe:
                    sf.Describe=Describe
                if Category:
                    sf.Category=Category
                if Price:
                    sf.Price=Price
                sf.save()
                message = {'code':'200',
                        'message': 'Cập nhật bản ghi thành công',
                        'data': SeaFoodSerializer(sf,context={'request': request}).data
                        }
                return Response(message,status=status.HTTP_200_OK)
            else:
                message = {'code':'401',
                        'message': 'Bạn không có quyền thục hiện chức năng này',
                        }
                return Response(message,status=status.HTTP_401_UNAUTHORIZED)
        else:
            message = {'code':'401',
                        'message': 'Cần xác thực trước khi thực hiện chức năng này',
                        }
            return Response(message,status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            if request.user.is_staff:
                sf = SeaFood.objects.get(pk=pk)
                sf.delete()
                message = {'code':'200',
                        'message': 'Xóa thành công',
                        }
                return Response(message,status=status.HTTP_200_OK)
            else:
                message = {'code':'401',
                        'message': 'Bạn không có quyền thục hiện chức năng này',
                        }
                return Response(message,status=status.HTTP_401_UNAUTHORIZED)
        else:
            message = {'code':'401',
                        'message': 'Cần xác thực trước khi thực hiện chức năng này',
                        }
            return Response(message,status=status.HTTP_401_UNAUTHORIZED)
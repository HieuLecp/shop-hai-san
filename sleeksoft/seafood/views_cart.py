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

import json

# @swagger_auto_schema(method='post', request_body=CustomerSerializer)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'list_id_product': openapi.Schema(type=openapi.TYPE_STRING),
                        },
                        required=['list_id_product'],
                    ),
    operation_summary="Thêm sản phẩm vào giỏ hàng - dữ liệu gửi dạng '[1,2]' - các id cần xóa nằm trong mảng ",
    operation_description="Thêm sản phẩm vào giỏ hàng - dữ liệu gửi dạng '[1,2]' - các id cần xóa nằm trong mảng",
    tags=['Giỏ hàng']
)
@swagger_auto_schema(
    method='delete',
    request_body=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'list_id_product': openapi.Schema(type=openapi.TYPE_STRING),
                        },
                        required=['list_id_product'],
                    ),
    operation_summary="Xóa sản phẩm khỏi giỏ hàng - dữ liệu gửi dạng '[1,2]' - các id cần xóa nằm trong mảng",
    operation_description="Xóa sản phẩm khỏi giỏ hàng - dữ liệu gửi dạng '[1,2]' - các id cần xóa nằm trong mảng",
    tags=['Giỏ hàng']
)
@api_view(['POST','DELETE'])
def Cart_data(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            list_id_product = request.data.get('list_id_product')
            print('list_id_product:',list_id_product)
            list_id_product = json.loads(list_id_product)
            print('list_id_product_js:',list_id_product)
            cart = request.user.Cart_product            
            # Lấy danh sách các sản phẩm hiện có trong giỏ hàng
            current_products = cart.List_product.all()
            # Xác định các sản phẩm mới cần thêm vào
            new_products = SeaFood.objects.filter(id__in=list_id_product).exclude(id__in=current_products)
            # Chỉ thêm các sản phẩm mới vào giỏ hàng
            for product in new_products:
                cart.List_product.add(product)
            # Lưu giỏ hàng
            cart.save()
            message = {'code':'200',
                   'message': 'Thêm sản phẩm vào giỏ hàng thành công',
                   }
            return Response(message,status=status.HTTP_200_OK)
        else:
            message = {'code':'401',
                        'message': 'Cần xác thực trước khi thực hiện chức năng này',
                        }
            return Response(message,status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            list_id_product = request.data.get('list_id_product')
            print('list_id_product:',list_id_product)
            list_id_product = json.loads(list_id_product)
            print('list_id_product_js:',list_id_product)
            cart = request.user.Cart_product            
            # Tìm sản phẩm cần xóa
            for i in list_id_product:
                product_to_remove = SeaFood.objects.get(id=i)
                # Xóa sản phẩm ra khỏi giỏ hàng
                cart.List_product.remove(product_to_remove)
            # Lưu giỏ hàng
            cart.save()
            message = {'code':'200',
                   'message': 'Xóa sản phẩm khỏi giỏ hàng thành công',
                   }
            return Response(message,status=status.HTTP_200_OK)
        else:
            message = {'code':'401',
                        'message': 'Cần xác thực trước khi thực hiện chức năng này',
                        }
            return Response(message,status=status.HTTP_401_UNAUTHORIZED)
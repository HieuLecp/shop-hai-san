from .models import *

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator


from django.http import HttpResponse
import requests
import time

from django.db import models
from django.utils import timezone

import os

from datetime import datetime

from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import datetime
from django.contrib import messages
import random
import string
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

import random
import string

import base64

import time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,parser_classes
from django.http import JsonResponse

import re
import json

def detail_page(request,pk):
    if request.method == 'GET':
        data = SeaFood.objects.get(pk=pk)
        context = {'data':data}
        return render(request, 'seafood/detail_page.html', context, status=200)
    

def home_page(request):
    if request.method == 'GET':
        data = SeaFood.objects.all()
        context = {'data':data}
        if 'error_login' in request.session:
            error = request.session.get('error_login')
            context ['error_login'] = error
            del request.session['error_login']
        return render(request, 'seafood/home_page.html', context, status=200)
    
def cart_page(request):
    if request.method == 'GET':
        context = {'name':'thái'}
        if request.user.is_authenticated:
            return render(request, 'seafood/cart_page.html', context, status=200)
        else:
            return redirect('login_page')
    
def admin_page(request):
    if request.method == 'GET':
        data_product = SeaFood.objects.all()
        context = {'data_product':data_product}
        if request.user.is_staff:
            return render(request, 'seafood/admin_page.html', context, status=200)
        else:
            return redirect('login_page')
    
def login_page(request):
    if request.method == 'GET':
        context = {'name':'thái'}
        return render(request, 'seafood/login_page.html', context, status=200)
        # if request.user.is_staff:
        #     return redirect('admin_page')
        # else:
        #     return render(request, 'seafood/login_page.html', context, status=200)

def register_page(request):
    if request.method == 'GET':
        context = {'name':'thái'}
        return render(request, 'seafood/register_page.html', context, status=200)
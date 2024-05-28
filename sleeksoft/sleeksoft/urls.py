"""th URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from Data_Interaction.admin import admin_site
from django.urls import path

from seafood.views_user import *
from seafood.views_seafood import *
from seafood.views_cart import *
from seafood.views import *
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import re_path,path


from django.views.generic.base import TemplateView
from django.conf.urls.static import serve

from django.views.generic import RedirectView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('user/', User_data,name='User_data'),
    path('user/<int:pk>/', User_detail,name='User_data'),
    path('user-authentication/', User_authentication,name='User_authentication'),
    path('keep-login/', Keep_login,name='Keep_login'),
    path('seafood/', Seafood_data,name='Seafood_data'),
    path('seafood/<int:pk>/', Seafood_detail,name='Seafood_detail'),
    path('cart/', Cart_data,name='Cart_data'),
    
    path('', home_page,name='home_page'),
    path('gio-hang/', cart_page,name='cart_page'),
    path('dang-nhap/', login_page,name='login_page'),
    path('dang-ky/', register_page,name='register_page'),
    path('admin/', admin_page,name='admin_page'),
    path('detail/', detail_page,name='detail_page'),
    
    path('detail-product/<int:pk>/', detail_page,name='detail_product'),
    
    
    
    
    # path('<slug:page_slug>/', views.trang_don,name='trang_don'),
    # path('<slug:page_slug>/<slug:page_filter>/<slug:page_key_filter>', views.trang_loc,name='trang_loc'),
    # path('thuong-hieu/<slug:page_filter>/', views.trang_thuong_hieu,name='trang_thuong_hieu'),
    # path('tim-kiem', views.trang_tim_kiem,name='trang_tim_kiem'),
    # path('chi-tiet/<slug:page_detail>/', views.trang_chi_tiet,name='trang_chi_tiet'),
    # path('dang-nhap', views.trang_dang_nhap,name='trang_dang_nhap'),
    # path('dang-xuat', views.dang_xuat,name='dang_xuat'),
    # path('dang-ki', views.trang_dang_ki,name='trang_dang_ki'),
    # path('doi-mat-khau', views.trang_doi_mat_khau,name='trang_doi_mat_khau'),
    # path('gio-hang', views.trang_gio_hang,name='trang_gio_hang'),
    # path('them-gio-hang', views.them_vao_gio_hang,name='them_vao_gio_hang'),
    # path('so-luong-gio-hang', views.thay_doi_so_luong_gio_hang,name='thay_doi_so_luong_gio_hang'),
    # path('xoa-gio-hang', views.xoa_gio_hang,name='xoa_gio_hang'),
    # path('xoa-het-gio-hang', views.xoa_het_gio_hang,name='xoa_het_gio_hang'),
    # path('don-dat-hang', views.don_dat_hang,name='don_dat_hang'),
    # path('xoa-don-hang',views.xoa_don_hang, name='xoa_don_hang'),
    # path('thong-tin-tai-khoan/<slug:user_id>/', views.trang_thong_tin_tai_khoan,name='trang_thong_tin_tai_khoan'),
    # path('study/revenue', views.trang_doanh_thu,name='trang_doanh_thu'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 
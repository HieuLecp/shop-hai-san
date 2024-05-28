from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

# Create your models here.

class SeaFood(models.Model):
    class Meta:
        ordering = ["id"]
    Name = models.CharField('Tên sản phẩm',max_length=100, null=True, blank=True)
    Describe = models.TextField('Mô tả', null=True, blank=True)
    Category = models.CharField('Danh mục',max_length=100, null=True, blank=True)
    Price = models.CharField('Giá',max_length=100, null=True, blank=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    
class Image_SeaFood(models.Model):
    class Meta:
        ordering = ["id"]
    Image = models.ImageField('Ảnh đại diện',upload_to='Image_SeaFood',null=True,blank=True)
    Belong_SeaFood = models.ForeignKey(SeaFood, on_delete=models.CASCADE, related_name='List_image')
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

class Cart(models.Model):
    class Meta:
        ordering = ["id"]
    List_product = models.ManyToManyField(SeaFood,null=True,blank=True,related_name='tist_product')
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

class Customer(AbstractUser):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Quản lý tài khoản Đăng nhập"
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('email').null = False
    AbstractUser._meta.get_field('username').blank = False
    AbstractUser._meta.get_field('username').null = False
    AbstractUser._meta.get_field('password').blank = False
    AbstractUser._meta.get_field('password').null = False

    Name = models.CharField('Tên khách hàng',max_length=255)
    Phone = models.CharField('Số điện thoại khách hàng',max_length=15, blank=True, null=True)
    Address = models.CharField('Đại chỉ khách hàng',max_length=255, blank=True, null=True)
    Birthday = models.DateField('Ngày sinh khách hàng',blank=True, null=True)
    Avatar = models.ImageField(upload_to='User_image',null=True,blank=True)
    Cart_product = models.OneToOneField(Cart,on_delete=models.CASCADE, related_name='cart_product',null=True,blank=True)
    Update_time = models.DateTimeField(auto_now=True)



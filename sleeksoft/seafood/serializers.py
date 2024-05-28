from rest_framework import serializers,validators
from .models import *
from rest_framework.validators import ValidationError
from django.conf import settings 
from rest_framework.response import Response
from rest_framework import status
import requests

class Image_SeaFoodSerializer(serializers.ModelSerializer):
    Image = serializers.SerializerMethodField()
    class Meta:
        model = Image_SeaFood
        fields = '__all__'
    def get_Image(self, instance):
        if instance.Image:
            return self.context['request'].build_absolute_uri(instance.Image.url)
        return None
class SeaFoodSerializer(serializers.ModelSerializer):
    List_image = Image_SeaFoodSerializer(many=True)
    class Meta:
        model = SeaFood
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    List_product = SeaFoodSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    Cart_product = CartSerializer()
    class Meta:
        model = Customer
        fields = '__all__'
        # write_only_fields = ['password']
        extra_kwargs = {
            'password': {'write_only': True},
            'last_login': {'write_only': True},
            'is_superuser': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'is_active': {'write_only': True},
            'date_joined': {'write_only': True},
            'Name': {'write_only': True},
            'Phone': {'write_only': True},
            'Address': {'write_only': True},
            'Birthday': {'write_only': True},
            'Avatar': {'write_only': True},
            # 'Update_time': {'write_only': True},
            'groups': {'write_only': True},
            'user_permissions': {'write_only': True},
        }

class Image_SeaFoodSerializer(serializers.ModelSerializer):
    Image = serializers.SerializerMethodField()
    class Meta:
        model = Image_SeaFood
        fields = '__all__'
    def get_Image(self, instance):
        if instance.Image:
            return self.context['request'].build_absolute_uri(instance.Image.url)
        return None
    

class SeaFoodSerializer(serializers.ModelSerializer):
    List_image = Image_SeaFoodSerializer(many=True)
    class Meta:
        model = SeaFood
        fields = '__all__'

# serializers.py
from rest_framework import serializers
from .models import User

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'address', 'country', 'birth_date', 'role', 
                  'login_at', 'registered_at']
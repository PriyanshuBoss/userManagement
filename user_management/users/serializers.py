from rest_framework import serializers
from mongoengine import Document
from .models import User

class UserSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    dob = serializers.DateField()
    address = serializers.CharField(max_length=255)
    gender = serializers.ChoiceField(choices=['male', 'female', 'other'])
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15)
    
    def create(self, validated_data):
        """Create a new User document"""
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing User document"""
        instance.update(**validated_data)
        return instance

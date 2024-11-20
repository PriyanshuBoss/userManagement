# serializers.py
from rest_framework import serializers
import uuid
from rest_framework.exceptions import ValidationError
from mongo_utilities import MongoConn

class UserSerializer(serializers.Serializer):
    user_id = serializers.CharField(read_only=True)
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    dob = serializers.CharField()
    address = serializers.CharField(max_length=255)
    gender = serializers.ChoiceField(choices=['male', 'female', 'other'])
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        
        return value

    def validate_firstname(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("First name should be at least 2 characters long.")
        return value

    def validate_lastname(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Last name should be at least 2 characters long.")
        return value

    def validate_gender(self, value):
        if value not in ['male', 'female', 'other']:
            raise serializers.ValidationError("Gender must be 'male', 'female', or 'other'.")
        return value

    def validate_address(self, value):
        if not value:
            raise serializers.ValidationError("Address cannot be empty.")
        if len(value) > 255:
            raise serializers.ValidationError("Address is too long, should be less than 255 characters.")
        return value

    
    def validate(self, data):

        if data.get('firstname', '').lower() == data.get('lastname', '').lower():
            raise serializers.ValidationError("First name and last name cannot be the same.")

        return data


    def create(self, validated_data):
        validated_data['user_id'] = str(uuid.uuid4())
        validated_data = self.validate(validated_data)
        
        mongo_conn = MongoConn()
        mongo_conn.insert_data(validated_data, 'users')

        return validated_data


    def update(self, instance, validated_data):
        """
        Updates only the fields that have changed in MongoDB
        """
        # Constructing the update query
        update_data = {}

        # Only update the fields that have been changed
        for field, value in validated_data.items():
            # Use `$set` to only update the changed fields
            update_data[field] = value

        # If no fields were passed, raise an error (this might happen if validated_data is empty)
        if not update_data:
            raise ValidationError("No fields to update.")

        # Returning the update query to be used by the view for MongoDB update
        return {'$set': update_data}

# serializers.py
from mongo_utilities import MongoConn
from rest_framework import serializers
import uuid
from datetime import datetime
from rest_framework.exceptions import ValidationError

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

        """
        Validates the phone number field.
        """

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
        """
        Validates first name and last name is not same.
        """
        firstname = data.get('firstname', None)
        lastname = data.get('lastname', None)

        if firstname and lastname:
            if firstname.lower() == lastname.lower():
                raise serializers.ValidationError("First name and last name cannot be the same.")

        return data

    def validate_dob(self, value):
        """
        Validates the date of birth (dob) field.
        """
        try:
            dob = datetime.strptime(value, "%Y-%m-%d").date()
            
            if dob > datetime.now().date():
                raise serializers.ValidationError("Date of birth cannot be in the future.")

            return value

        except ValueError:
            # Raise an error if the format is invalid
            raise serializers.ValidationError("Invalid date format. Use YYYY-MM-DD.")


    def create(self, validated_data):
        validated_data['user_id'] = str(uuid.uuid4())
        validated_data = self.validate(validated_data)

        # with MongoConn() as mongo_conn:
        #     mongo_conn.insert_data(validated_data, 'users')
    
        return validated_data


    def update(self, instance, validated_data):
        """
        Updates only the fields that have changed in MongoDB
        """
        update_data = {}

        for field, value in validated_data.items():
            update_data[field] = value

        if not update_data:
            raise ValidationError("No fields to update.")

        return {'$set': update_data}

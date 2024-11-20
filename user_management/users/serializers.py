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

    def create(self, validated_data):
        # Generate a unique ID for the user (UUID)
        validated_data['user_id'] = str(uuid.uuid4())  # Using UUID v4 for unique ID
        
        mongo_conn = MongoConn()
        mongo_conn.insert_data(validated_data, 'users')  # Assuming 'insert_data' saves data in MongoDB

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

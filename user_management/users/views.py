# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from .serializers import UserSerializer
from mongo_utilities import MongoConn

class UserView(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            x = serializer.save()
            print(x)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def get(self, request, user_id=None):
        mongo_conn = MongoConn()
        
        if user_id:
            try:
                data = mongo_conn.fetch_data({'user_id': user_id}, 'users')
                
                if data:
                    serializer = UserSerializer(data[0])
                    
                    return Response(serializer.data)
                
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            data = mongo_conn.fetch_data({}, 'users')
            serializer = UserSerializer(data, many=True)
            
            return Response(serializer.data)

    def put(self, request, user_id):
        mongo_conn = MongoConn()

        try:
            data = mongo_conn.fetch_data({'user_id': user_id}, 'users')

            if not data:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            user = data[0]

            serializer = UserSerializer(user, data=request.data, partial=True)

            if not serializer.is_valid():
                return Response({'success': False, 'data': serializer.errors})

            update_query = serializer.update(user, serializer.validated_data)
            
            update_result = mongo_conn.update_data({'user_id': user_id}, update_query, 'users')

            if update_result.matched_count == 0:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            if update_result.modified_count == 0:
                return Response({'error': 'No changes made to user data'}, status=status.HTTP_400_BAD_REQUEST)

            updated_data = mongo_conn.fetch_data({'user_id': user_id}, 'users')
            
            if updated_data:
                updated_serializer = UserSerializer(updated_data[0])
                return Response({'success': True, 'data': updated_serializer.data})

            return Response({'success': True, 'data': serializer.data})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        mongo_conn = MongoConn()
        
        try:
            delete_result = mongo_conn.delete_data({'user_id': user_id}, 'users')
            
            if delete_result:
                return Response({'success': True})
            
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

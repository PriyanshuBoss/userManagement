# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from mongo_utilities import MongoConn

class UserView(APIView):
    
    #api to create the user
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            
            with MongoConn() as mongo_conn:
                validated_data = serializer.save()
                mongo_conn.insert_data(validated_data, 'users')
            
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    #api to fetch the user
    def get(self, request, user_id=None):
        
        try:
            with MongoConn() as mongo_conn:
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
        except Exception as e:
            return Response({'error': 'Unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #api to update user
    def put(self, request, user_id):
        
        try:
            with MongoConn() as mongo_conn:
                data = mongo_conn.fetch_data({'user_id': user_id}, 'users')
                
                if not data:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

                user = data[0]

                serializer = UserSerializer(user, data=request.data, partial=True)
                
                if not serializer.is_valid():
                    return Response({'success': False, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

                update_query = serializer.update(user, serializer.validated_data)
                
                update_result = mongo_conn.update_data({'user_id': user_id}, update_query, 'users')

                if update_result.matched_count == 0:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

                if update_result.modified_count == 0:
                    return Response({'error': 'No changes made to user data'}, status=status.HTTP_400_BAD_REQUEST)

                updated_data = mongo_conn.fetch_data({'user_id': user_id}, 'users')

                if updated_data:
                    updated_serializer = UserSerializer(updated_data[0])
                    return Response({'success': True, 'data': updated_serializer.data}, status=status.HTTP_200_OK)

                return Response({'error': 'Error fetching updated data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    #api to delete user
    def delete(self, request, user_id):
        try:
            with MongoConn() as mongo_conn:
                delete_result = mongo_conn.delete_data({'email': user_id}, 'users')

                if delete_result:
                    return Response({'success': True}, status=status.HTTP_200_OK)
                
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': 'An error occurred while processing the request', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)


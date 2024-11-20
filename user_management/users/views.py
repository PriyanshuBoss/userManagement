# views.py

from django.http import JsonResponse
from .models import User
import json
from mongo_utilities import MongoConn

def create_user(request):
    
    if request.method == 'GET':
        data = json.loads(request.body)

        mongo_conn = MongoConn()
        result = False
        result = mongo_conn.insert_data(data,'users')
        print(result)

    return JsonResponse({
        'success':True
    })

def fetch_users(request):
    
    if request.method == 'GET':

        mongo_conn = MongoConn()
        get = dict()
        data = mongo_conn.fetch_data(get,'users')
        user_list = [
            {**user, "_id": str(user["_id"])} for user in list(data)
        ]

        return JsonResponse(user_list, safe=False)


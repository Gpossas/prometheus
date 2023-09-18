from datetime import datetime, timedelta

from django.conf import settings
from django.http import JsonResponse

import jwt
import uuid

def generate_custom_jwt_token(user_uuid):
    jwt_secret_key = settings.SECRET_KEY
    payload = {
        'user_uuid': str(user_uuid), 
        'exp': datetime.utcnow() + timedelta(hours=1)  
    }

    token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')

    return token

def decode_and_set_cookie(request):
    jwt_token = request.COOKIES.get('jwt_token')

    if jwt_token:
        try:
            decoded_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_uuid = decoded_token.get('user_uuid')
        except jwt.ExpiredSignatureError:
            user_uuid = None
    else:
        user_uuid = uuid.uuid4()
        token = generate_custom_jwt_token(user_uuid)

        response = JsonResponse({'message': 'Token successfully generated'})
        response.set_cookie('jwt_token', token, max_age=3600)
    
    return user_uuid

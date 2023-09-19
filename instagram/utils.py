from datetime import datetime, timedelta

from django.conf import settings

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

def generate_data():
    user_uuid = uuid.uuid4()
    token = generate_custom_jwt_token(user_uuid)

    data = {
            'message': 'Token successfully generated',
            'user_uuid': user_uuid,
            'token': token,
        }

    return data
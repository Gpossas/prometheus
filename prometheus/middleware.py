from instagram.utils import generate_data
from datetime import datetime
import jwt
from django.conf import settings

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.SECRET_KEY = settings.SECRET_KEY
        self.token = ''
        self.user_uuid = ''
        

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.endswith("/"):
            jwt_token = request.COOKIES.get('jwt')
            
            if jwt_token:
                try:
                    payload = jwt.decode(jwt_token, self.SECRET_KEY, algorithms=["HS256"])
                    current_time = datetime.utcnow()

                    if 'exp' in payload and payload['exp'] < current_time.timestamp():
                       response.delete_cookie('jwt')    

                    return response
                
                except jwt.ExpiredSignatureError as expired_token:
                    response.delete_cookie('jwt')
                    return response
                
                except jwt.DecodeError as decode_error:
                    response.delete_cookie('jwt')
                    return response
                
                except jwt.InvalidTokenError as invalid_token:
                    response.delete_cookie('jwt')
                    return response

                except Exception as e:
                    response.delete_cookie('jwt')
                    return response

            else:
                data = generate_data()

                self.user_uuid = data['user_uuid']
                self.token = data['token']

                response.set_cookie("jwt", value=self.token, expires=3600)

                return response
        
        else:
            return response
        
    
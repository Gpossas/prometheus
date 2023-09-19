from django.http import HttpResponse
from jose.backends import RSAKey
from jose.jwt import decode
from django.core.cache import cache
from instagram.utils import generate_data

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.RSA_PUBLIC_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCpB03oE0Aeczx0p6ztckTkf22NwZiHsoyTnhKVJ3ZT6Nk1s3gIIHqFrDgLmRvCsssjWt3xaLKJigfhtpmi4ZUhp100nBQSaA0QgUcs//qyXMvKs/Wl69iYCxBWLw4c7lWEh5m2ayXDM1Sf7+C/GptOiCE3J2L4b29C+fcqHY3UtF+RXI0u3MQy+iae3a+m42FMs6gS6fHcSf8l2giLcRSVWBofaiPjG5u1fKypCan0wMAEIt9jFm60W9NautKe64GgZ5nYay9qMqFC1KwZmDL17a5SbIUTaGcNhiYDcP9mCMWEoa+wmfuk+BsyINaCS5TDZ7KdZP7Ny0jFFxQ4BdpJj2exqd3V9iahobERfv7Fjn8apRHEW1Nr4DBAfBm8yv6Dc3SEwxrO4Upj09pIIwYuFs5CSfLAgDWLYfH7rDeB5+KKoNwGQIcwUIqX1fIPcyhiH1DLL42/4yfrBD2xigVDmmnw9qE1+fEni/3lzK0iP/DpudPb/iqt4BjOkH+gS/c= slocksert@noob-2023-09-17' #this is a ssh key that can be generated using the command 'sh-keygen -t rsa -b 2048 -f my_rsa_key'
        self.token = ''
        self.user_uuid = ''
        

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.endswith("/"):
            jwt_token = request.COOKIES.get('jwt')
            
            if jwt_token:
                try:
                    return response

                except Exception:
                    response.set_cookie("jwt", value=None, expires=3600)
            else:
                data = generate_data()

                self.user_uuid = data['user_uuid']
                self.token = data['token']

            response.set_cookie("jwt", value=self.token, expires=3600)

            return response
        
        else:
            return response
        
    
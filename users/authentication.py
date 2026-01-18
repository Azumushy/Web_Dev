from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class IPRestrictedJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        user, token = result
        token_ip = token.get("ip")
        request_ip = request.META.get("REMOTE_ADDR")
        if token_ip and token_ip != request_ip:
            raise AuthenticationFailed("Token IP mismatch")
        return user, token

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class QueryParameterTokenAuthentication(TokenAuthentication):
    """
    Extend TokenAuthentication to accept tokens via query parameter 'token'.
    """
    def authenticate(self, request):
        # Check for token in query parameters
        token = request.query_params.get('token')
        if token:
            return self.authenticate_credentials(token)
        return super().authenticate(request)

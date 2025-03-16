from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.exceptions import PermissionDenied


class OAuth2WithClientUserAuth(OAuth2Authentication):
    """
    This Authentication Class ensures that:
    - a user is set to the request
    - if no user is set on the request it will extract it from the application (case for client_credential)
    - the user hs to be active
    """

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        user, token = result
        if not user:
            if token.application.user:
                user = token.application.user
            else:
                raise PermissionDenied(
                    f'The Client {token.application.client_id} has no user assigned'
                )
        if not user.is_active:
            raise PermissionDenied(
                f'The User {user} is not active'
            )
        return (user, token)

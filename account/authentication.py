from typing import Optional

from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse


class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """

    def authenticate(self, request: HttpRequest, username: str = None, password: str = None) -> Optional[User]:
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass

        return None

    def get_user(self, user_id) -> Optional[User]:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

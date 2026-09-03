from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


@database_sync_to_async
def get_user(user_id):
    User = get_user_model()

    try:
        return User.objects.get(
            id=user_id,
            is_active=True
        )
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):

        query_string = scope.get("query_string", b"").decode()

        print(f"🔍 DEBUG: Query string = {query_string[:60]}")

        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        print(f"🔍 DEBUG: Token extrait = {token is not None}")

        scope["user"] = AnonymousUser()

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token["user_id"]

                scope["user"] = await get_user(user_id)

                print(
                    f"🔍 DEBUG: User dans scope = "
                    f"{scope['user']}"
                )

            except (TokenError, KeyError, TypeError, ValueError) as e:
                print(f"🔍 DEBUG: Token invalide = {e}")

        return await super().__call__(
            scope,
            receive,
            send
        )

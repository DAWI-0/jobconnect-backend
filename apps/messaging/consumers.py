import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print(f"🔍 CONSUMER: user dans scope = {self.scope.get('user')}")

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"
        self.user = self.scope.get("user")

        # Vérification authentification
        if not self.user or self.user.is_anonymous:
            print("🔍 CONSUMER: PAS D'UTILISATEUR → fermeture")
            await self.close(code=4401)
            return

        print(
            f"🔍 CONSUMER: User = {self.user.email}, "
            f"test participation..."
        )

        # Vérification participation à la conversation
        if not await self.is_participant():
            print("🔍 CONSUMER: PAS PARTICIPANT → fermeture")
            await self.close(code=4403)
            return

        print("🔍 CONSUMER: ACCEPTÉ !")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f"🔌 CONSUMER: Déconnexion, code = {close_code}")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            print("❌ CONSUMER: JSON invalide")
            return

        message = data.get("message", "")

        if not isinstance(message, str):
            return

        message = message.strip()

        if not message:
            return

        saved = await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user.id,
                "sender_email": self.user.email,
                "sender_name": (
                    f"{self.user.first_name} "
                    f"{self.user.last_name}"
                ).strip() or self.user.email,
                "message_id": saved["id"],
                "created_at": saved["created_at"],
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(event)
        )

    @database_sync_to_async
    def is_participant(self):
        try:
            conv = Conversation.objects.select_related(
                "candidate__user",
                "recruiter__user"
            ).get(id=self.conversation_id)

            candidate_user = conv.candidate.user
            recruiter_user = conv.recruiter.user

            print(
                f"🔍 candidate={candidate_user.email}, "
                f"recruiter={recruiter_user.email}, "
                f"me={self.user.email}"
            )

            return (
                self.user.id == candidate_user.id
                or self.user.id == recruiter_user.id
            )

        except Conversation.DoesNotExist:
            print("🔍 CONSUMER: Conversation inexistante")
            return False

        except Exception as e:
            print(f"🔍 ERREUR is_participant: {e}")
            return False

    @database_sync_to_async
    def save_message(self, content):
        conv = Conversation.objects.get(
            id=self.conversation_id
        )

        # Vérification supplémentaire de sécurité
        if self.user.id not in {
            conv.candidate.user_id,
            conv.recruiter.user_id,
        }:
            raise PermissionError(
                "Vous ne participez pas à cette conversation."
            )

        msg = Message.objects.create(
            conversation=conv,
            sender=self.user,
            content=content
        )

        # Mettre à jour la conversation
        Conversation.objects.filter(
            id=conv.id
        ).update(
            updated_at=timezone.now()
        )

        return {
            "id": msg.id,
            "created_at": msg.created_at.isoformat(),
        }

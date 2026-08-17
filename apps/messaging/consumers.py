from apps.messaging.models import Conversation
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"🔍 CONSUMER: user dans scope = {self.scope.get('user')}")
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"
        self.user = self.scope.get("user")

        if not self.user:
            print("🔍 CONSUMER: PAS D'UTILISATEUR → fermeture")
            await self.close()
            return

        print(f"🔍 CONSUMER: User = {self.user.email}, test participation...")

        if not await self.is_participant():
            print("🔍 CONSUMER: PAS PARTICIPANT → fermeture")
            await self.close()
            return

        print("🔍 CONSUMER: ACCEPTÉ !")
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        if not message.strip():
            return

        saved = await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user.id,
                "sender_email": self.user.email,
                "sender_name": f"{self.user.first_name} {self.user.last_name}".strip() or self.user.email,
                "message_id": saved["id"],
                "created_at": saved["created_at"],
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def is_participant(self):
        from .models import Conversation
        try:
            conv = Conversation.objects.select_related(
                "candidate__user", "recruiter__user"
            ).get(id=self.conversation_id)

            candidate_user = conv.candidate.user if conv.candidate else None
            recruiter_user = conv.recruiter.user if conv.recruiter else None

            print(f"🔍 candidate={candidate_user}, recruiter={recruiter_user}, me={self.user}")
            return self.user == candidate_user or self.user == recruiter_user

        except Conversation.DoesNotExist:
            print("🔍 CONSUMER: Conversation inexistante")
            return False
        except Exception as e:
            print(f"🔍 ERREUR is_participant: {e}")
        return False

    @database_sync_to_async
    def save_message(self, content):
        from .models import Message, Conversation
        conv = Conversation.objects.get(id=self.conversation_id)
        msg = Message.objects.create(conversation=conv, sender=self.user, content=content)
        return {"id": msg.id, "created_at": str(msg.created_at)}
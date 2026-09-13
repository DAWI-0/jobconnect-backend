import os
import django
import asyncio

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

django.setup()

from channels.layers import get_channel_layer


async def test():
    layer = get_channel_layer()

    await layer.group_add(
        "test_group",
        "test_channel"
    )

    print("GROUP_ADD OK")

    await layer.group_send(
        "test_group",
        {
            "type": "test.message",
            "text": "hello"
        }
    )

    print("GROUP_SEND OK")


asyncio.run(test())

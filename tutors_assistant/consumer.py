import asyncio
import json
import logging
import os

import aio_pika
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.config.settings")
django.setup()

from bot.loader import dp


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    connection = await aio_pika.connect_robust(host="rabbitmq", port=5672)

    queue_name = "homework"

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    message = json.loads(message.body)
                    await dp.bot.send_message(
                        chat_id=message["chat_id"], text=message["message"]
                    )


if __name__ == "__main__":
    asyncio.run(main())

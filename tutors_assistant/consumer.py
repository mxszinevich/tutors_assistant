import asyncio
import logging
import os

import aio_pika
import django

from rabbitmq_utils import Message, chat_send_message

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.config.settings")
django.setup()

from bot.loader import dp


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    connection = await aio_pika.connect_robust(host=os.getenv("HOSTNAME_RABBITMQ"), port=os.getenv("PORT_RABBITMQ"))

    queue_name = "homework"

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        rabbit_message = Message()
                        rabbit_message.load_data(data=message.body)
                        await chat_send_message(dp=dp, message=rabbit_message)
                    except ValueError:
                        pass


if __name__ == "__main__":
    asyncio.run(main())

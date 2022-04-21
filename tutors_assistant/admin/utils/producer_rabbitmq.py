import os

import pika


def producer(message: str):
    """
    Отправка сообщения о создании нового домашнего задания в очередь
    """
    try:
        parameters = pika.ConnectionParameters(
            host=os.getenv("HOSTNAME_RABBITMQ"), port=os.getenv("PORT_RABBITMQ")
        )
        connection = pika.BlockingConnection(parameters=parameters)
        channel = connection.channel()
    except pika.exceptions.AMQPConnectionError:
        return

    channel.queue_declare(queue="homework")
    channel.basic_publish(exchange="", routing_key="homework", body=message)
    connection.close()

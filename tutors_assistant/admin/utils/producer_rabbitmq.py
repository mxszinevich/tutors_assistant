import pika


def producer(message: str):
    """
    Отправка сообщения о создании нового домашнего задания в очередь
    """

    parameters = pika.ConnectionParameters(host="rabbitmq", port=5672)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    channel.queue_declare(queue="homework")
    channel.basic_publish(exchange="", routing_key="homework", body=message)
    connection.close()

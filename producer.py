import pika
from models import Users
from connect import connect

import bson.json_util as json_util
from faker import Faker

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')

NUMBER_USERS = 10
fake = Faker()


def main():
    for i in range(NUMBER_USERS):
        users = Users(fullname=fake.name(),
                      email=fake.email(),
                      status=True)
        users.save()

        message = {
            "ObjectID": users.id,
            "email_text": "Some text"
        }

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json_util.dumps(message).encode(),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        print(" [x] Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    main()


from confluent_kafka import Producer
import os

def delivery_callback(err, msg):
    if err:
        print("Message delivery failed:", err)
    else:
        print("Message delivered to", msg.topic(), "-", msg.partition())

def produce_messages(producer, folder_path, topic):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, 'rb') as file:
                data = file.read()
                producer.produce(topic, data, callback=delivery_callback)
                producer.poll(0)

def main():
    kafka_bootstrap_servers = 'localhost:9092'
    kafka_topic = 'music_topic'
    folder_path = 'fma'

    conf = {'bootstrap.servers': kafka_bootstrap_servers}
    producer = Producer(**conf)

    produce_messages(producer, folder_path, kafka_topic)

    producer.flush()

if __name__ == '__main__':
    main()

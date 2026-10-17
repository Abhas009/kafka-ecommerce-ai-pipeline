import os
import json
import time
import random
from datetime import datetime
from faker import Faker
from kafka import KafkaProducer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Faker
fake = Faker()

# Aiven Kafka Configuration (Notice the ssl_cafile)
conf = {
    'bootstrap_servers': os.getenv('KAFKA_BROKER'),
    'security_protocol': 'SASL_SSL',
    'sasl_mechanism': 'SCRAM-SHA-256',
    'sasl_plain_username': os.getenv('KAFKA_USERNAME'),
    'sasl_plain_password': os.getenv('KAFKA_PASSWORD'),
    'ssl_cafile': 'ca.pem', 
    'value_serializer': lambda v: json.dumps(v).encode('utf-8')
}

print("Connecting to Aiven Kafka...")
producer = KafkaProducer(**conf)
topic_name = 'ecommerce_events'

print(f"Connected! Sending events to topic '{topic_name}'...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        # Create a fake e-commerce event
        event = {
            "event_id": fake.uuid4(),
            "timestamp": datetime.now().isoformat(),
            "user_id": fake.random_int(min=1000, max=9999),
            "event_type": random.choices(
                ["page_view", "add_to_cart", "purchase"], 
                weights=[70, 20, 10], 
                k=1
            )[0],
            "product_id": f"PROD-{fake.random_int(min=100, max=999)}",
            "price": round(random.uniform(10.0, 500.0), 2) if random.random() > 0.7 else 0.0
        }
        
        # Send to Kafka
        producer.send(topic_name, value=event)
        producer.flush() 
        
        print(f"Sent: {event['event_type']} | User: {event['user_id']} | Price: ${event['price']}")
        
        # Wait 1 second before sending the next event
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping producer...")
finally:
    producer.close()
    print("Producer closed.")
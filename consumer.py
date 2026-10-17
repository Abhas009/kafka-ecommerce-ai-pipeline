import os
import json
import duckdb
from kafka import KafkaConsumer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Kafka Configuration (Same as producer, but using KafkaConsumer)
conf = {
    'bootstrap_servers': os.getenv('KAFKA_BROKER'),
    'security_protocol': 'SASL_SSL',
    'sasl_mechanism': 'SCRAM-SHA-256',
    'sasl_plain_username': os.getenv('KAFKA_USERNAME'),
    'sasl_plain_password': os.getenv('KAFKA_PASSWORD'),
    'ssl_cafile': 'ca.pem',
    'group_id': 'ecommerce-consumer-group',
    'auto_offset_reset': 'earliest', # Start reading from the beginning
    'value_deserializer': lambda x: json.loads(x.decode('utf-8'))
}

print("Connecting to DuckDB...")
conn = duckdb.connect('streaming_data.duckdb')

# Create the table where we will store the live data
conn.execute("""
    CREATE TABLE IF NOT EXISTS live_events (
        event_id VARCHAR,
        timestamp TIMESTAMP,
        user_id INTEGER,
        event_type VARCHAR,
        product_id VARCHAR,
        price DOUBLE
    )
""")
print("Table 'live_events' is ready.")

print("Connecting to Aiven Kafka...")
consumer = KafkaConsumer('ecommerce_events', **conf)

print("Listening for live events. Press Ctrl+C to stop.\n")

try:
    for message in consumer:
        event = message.value
        
        # Insert the event into DuckDB
        conn.execute("""
            INSERT INTO live_events (event_id, timestamp, user_id, event_type, product_id, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            event['event_id'], 
            event['timestamp'], 
            event['user_id'], 
            event['event_type'], 
            event['product_id'], 
            event['price']
        ))
        
        print(f"Stored in DuckDB: {event['event_type']} | User: {event['user_id']}")

except KeyboardInterrupt:
    print("\nStopping consumer...")
finally:
    consumer.close()
    conn.close()
    print("Consumer closed.")
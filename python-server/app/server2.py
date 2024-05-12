import pika
import json
import time
from threading import Thread

class TaskProcessor(Thread):
    def __init__(self, connection_params, queue_name, method, properties, body):
        super().__init__()
        self.connection_params = connection_params
        self.queue_name = queue_name
        self.method = method
        self.properties = properties
        self.body = body

    def run(self):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()

        try:
            # Declare the queue
            channel.queue_declare(queue=self.queue_name)

            # Convert the received message from JSON
            task = json.loads(self.body)
            print(" [x] Received task:", task)
            self.constructObject(task)




            #time.sleep(1)  # Sleep for 1 second to simulate processing

            print(" [x] Task processed successfully.")
            # Manually acknowledge the message
            #channel.basic_ack(delivery_tag=self.method.delivery_tag)
        except Exception as e:
            print(f"Error processing task: {e}")
            # Log the error or implement retry logic here
        finally:
            # Close the connection
            connection.close()


    def constructObject(self , task):
        image_array_uuid = task['imageArrayUUID']
        print("Image Array UUID:", image_array_uuid)

        # Accessing the 'images' key which contains a list of dictionaries
        images = task['images']
        print("Images:")
        for image in images:
            # Accessing the 'id', 'imgUrl', and 'mimeType' keys inside each image dictionary
            image_id = image['id']
            image_url = image['imgUrl']
            image_mime_type = image['mimeType']

            print("  Image ID:", image_id)
            print("  Image URL:", image_url)
            print("  Image MIME Type: ",image_mime_type)
        

# Define the RabbitMQ connection parameters
connection_params = pika.ConnectionParameters('localhost')

def callback(ch, method, properties, body):
    # Create and start a new TaskProcessor thread for each message
    TaskProcessor(connection_params, 'process_images', method, properties, body).start()

# Create a separate connection and channel for the consumer
consumer_connection = pika.BlockingConnection(connection_params)
consumer_channel = consumer_connection.channel()
# Set up the consumer with auto_ack=False
consumer_channel.basic_consume(queue='process_images', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
consumer_channel.start_consuming()
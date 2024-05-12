// queueListener.mjs

import amqp from 'amqplib';
import sessionStore from './sessionStore.js';

async function listenToQueue() {
    try {
        const connection = await amqp.connect('amqp://macbook'); // Connect to the message queue service
        const channel = await connection.createChannel(); // Create a channel
        const queueName = 'finished_processing'; // Specify the queue name

        await channel.assertQueue(queueName); // Ensure the queue exists

        console.log('Waiting for messages...');

        // Consume messages from the queue
        channel.consume(queueName, (message) => {
            if (message !== null) {
                // Process the message
                console.log('Received message:', message.content.toString());
                // Acknowledge the message
                channel.ack(message);
            }
        });
    } catch (error) {
        console.error('Error listening to queue:', error);
    }
}

export { listenToQueue };

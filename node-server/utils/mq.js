import amqp from 'amqplib';

const publishTask = async (imageObjects) => {
  try {
    console.log('adsf')
    const connection = await amqp.connect('amqp://macbook');

    const channel = await connection.createChannel();
      await channel.assertQueue('process_images', { durable: false });

      // Convert imageObjects to JSON string
      const taskJson = JSON.stringify(imageObjects);

      // Publish the task to the queue
      channel.sendToQueue('process_images', Buffer.from(taskJson));
      console.log(` [x] Task sent: ${taskJson}`);

      // Close the connection
      await channel.close();
      await connection.close();
  } catch (error) {
      console.error(`Error publishing tasks: ${error}`);
  }
}


export default publishTask
// Adapted from https://discord.com/channels/595317990191398933/967783711955365899/983757031573958676

import * as mqtt from 'mqtt';
require('dotenv').config()

let topic = "example-topic";

const client = mqtt.connect(process.env.PUBSUB_ENDPOINT, {
    port: Number(process.env.PUBSUB_PORT),
    username: "anything",
    password: process.env.BROKER_TOKEN.replace(/['"]+/g, ''),
    connectTimeout: 2000, // 2 seconds
    protocolVersion: 5,
    clean: true,
    clientId: ""
});

client.on("error", function (err) {
    console.log(`⚠️  error: ${err}`);
    client.end();
    process.exit();
});

// Connect to your broker
client.on("connect", function () {
    console.log(`🌎 connected!`);
    // Subscribe to a topic
    client.subscribe(topic, function (err) {
        if (!err) {
            console.log(`✅ subscribed to ${topic}`);
            // Publish a message!
            client.publish(topic, "Hello from NodeJS Typescript!");
        }
    });
});

// Start waiting for messages
client.on("message", async function (topic, message) {
    console.log(`received a message: ${message.toString()}`);
});
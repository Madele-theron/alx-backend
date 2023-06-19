import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();
const asyncGet = promisify(client.get).bind(client)
const asyncSet = promisify(client.set).bind(client)

// Task 1 
client.on('error', (error) => {
    console.log(`Redis client not connected to the server: ${error.message}`);
});

client.once('connect', () => {
    console.log('Redis client connected to the server');
});

// Task 3 - change to async / await
async function setNewSchool(schoolName, value) {
    await asyncSet(schoolName, value)
    .then((response) => {
        redis.print(`Reply: ${response}`)
    })
}

async function displaySchoolValue(schoolName) {
        console.log(await asyncGet(schoolName));
    }

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

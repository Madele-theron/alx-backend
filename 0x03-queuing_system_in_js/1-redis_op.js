import redis from 'redis';

const client = redis.createClient();

// Task 1 
client.on('error', (error) => {
    console.log(`Redis client not connected to the server: ${error.message}`);
});

client.once('connect', () => {
    console.log('Redis client connected to the server');
});

// Task 2
function setNewSchool(schoolName, value) {
    client.set(schoolName, value, redis.print);
}

function displaySchoolValue(schoolName) {
    client.get(schoolName, (error, response) => {
        console.log(reponse);
    });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

import kue from 'kue';
import redis from 'redis';
import { promisify } from 'util';
import express from 'express';

const client = redis.createClient();
const queue = kue.createQueue();

const app = express();
const PORT = 1245;

const clientGet = promisify(client.get).bind(client);
const clientSet = promisify(client.set).bind(client);

const reserveSeat = async (number) =>  await clientSet('available_seats', number);
const getCurrentAvailableSeats = async () => await clientGet('available_seats');

let reservationEnabled;

// ROUTES

app.get('/available_seats', async (request, response) => {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    response.json({numberOfAvailableSeats});
});

  app.get('/reserve_seat', async (request, response) => {
    if (!reservationEnabled) response.json({ "status": "Reservation are blocked" });
    let availableSeats = await getCurrentAvailableSeats();
    const job = queue.create('reserve_seat', {availableSeats}).save((error) => {
      if (!error) {
        response.json({ status: 'Reservation in process' });
      } else {
        response.json({ status: 'Reservation failed' });
      };
    });
    job.on('failed', (error) => console.log(`Seat reservation job ${job.id} failed: ${error}`));
    job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
});

  app.get('/process', async (request, response) => {
      queue.process('reserve_seat', async (job, done) => {
        console.log(job.data.availableSeats);
        let availableSeats = await getCurrentAvailableSeats();
        if (job.data.availableSeats <= 0) done(Error('Not enough seats available'));
        const updatedAvailableSeats = Number(job.data.availableSeats) - 1
        await reserveSeat(updatedAvailableSeats);
        if (updatedAvailableSeats === 0) reservationEnabled = false;
        done();
      });
      response.json({ status: 'Queue processing' });
});

// SERVER
  app.listen(PORT, () => {
    reserveSeat(50);
    reservationEnabled = true;
    console.log('Server is Running in port ' + PORT)
  });

import kue from 'kue';
const queue = kue.createQueue();

const jobInfo = {
    phoneNumber: "3240861107",
    message: "This is message of test"
}

const job = queue.create('push_notification_code', jobInfo).save((error) => {
    if( !error ) console.log(`Notification job created: ${job.id}`);
})

job.on('complete', () => {
    console.log('Job completed with data ');
});

job.on('failed', (err, done) => {
    console.log('Notification job completed');
})
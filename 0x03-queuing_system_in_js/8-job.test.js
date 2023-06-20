import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';
const queue = kue.createQueue();

const jobInfo = [
    {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
    },
];

describe('createPushNotificationsJobs', () => {
    before(() => {
        queue.testMode.enter();
    });

    afterEach(() => {
        queue.testMode.clear();
    });

    after(() => {
        queue.testMode.exit();
    });

    it('display a error message if jobs is not an array passing Number', () => {
        expect(() => {
        createPushNotificationsJobs(2, queue);
        }).to.throw('Jobs is not an array');
    });

    it('display a error message if jobs is not an array passing Object', () => {
        expect(() => {
        createPushNotificationsJobs({}, queue);
        }).to.throw('Jobs is not an array');
    });

    it('display a error message if jobs is not an array passing String', () => {
        expect(() => {
        createPushNotificationsJobs('Hello', queue);
        }).to.throw('Jobs is not an array');
    });

    it('should NOT display a error message if jobs is an array with empty array', () => {
        const ret = createPushNotificationsJobs([], queue);
        expect(ret).to.equal(undefined);
    });

    it('create two new jobs to the queue', () => {
        queue.createJob('thisJob', { foo: 'bar' }).save();
        queue.createJob('thatJob', { baz: 'bip' }).save();
        expect(queue.testMode.jobInfo.length).to.equal(2);
        expect(queue.testMode.jobInfo[0].type).to.equal('thisJob');
        expect(queue.testMode.jobInfo[0].data).to.eql({ foo: 'bar' });
        expect(queue.testMode.jobInfo[1].type).to.equal('thatJob');
        expect(queue.testMode.jobInfo[1].data).to.eql({ baz: 'bip' });
    });
});

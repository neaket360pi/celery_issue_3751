import requests
from celery import Celery
import json
import logging

import constants


logger = logging.getLogger('celery_app')
logger.setLevel(logging.INFO)

app = Celery(
    'worker@example.com'
)

app.conf.update({
    'broker_url': constants.BROKER_URL,
    'worker_max_tasks_per_child': 1
})


@app.task()
def stuff(queue_name):
    logger.debug('do stuff...')

    remove_queue.delay(queue_name)


@app.task()
def remove_queue(queue_name):
    logger.debug('deleting queue {}'.format(queue_name))

    app.control.cancel_consumer(
        queue_name
    )

    delete_rabbitmq_queue(queue_name)


def create_rabbitmq_queue(queue_name):
    url = '{}/queues/%2f/{}'.format(constants.BROKER_API_URL, queue_name)

    body = {
        'auto_delete': False,
        'durable': True,
        'arguments': []
    }

    logger.debug('Creating queue {} on rabbitmq'.format(queue_name))
    r = requests.put(
        url,
        data=json.dumps(body),
        headers={'Content-Type': 'application/json'},
        auth=(constants.BROKER_API_USER, constants.BROKER_API_PASS)
    )
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.exception(
            'Error - failed to create queue {}'.format(queue_name)
        )


def delete_rabbitmq_queue(queue_name):
    url = "{0}/queues/%2f/{1}".format(constants.BROKER_API_URL, queue_name)

    r = requests.delete(
        url,
        auth=(constants.BROKER_API_USER, constants.BROKER_API_PASS)
    )
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.exception('Error - to delete queue {}'.format(queue_name))


@app.task()
def add_queue(queue_name):
    try:
        create_rabbitmq_queue(queue_name)
    except Exception as e:
        logger.exception('Error - failed to create queue on rabbitmq')

    app.control.add_consumer(
        queue_name
    )
    logger.debug('Added queue {}'.format(queue_name))

    stuff.apply_async(args=[queue_name], queue=queue_name)

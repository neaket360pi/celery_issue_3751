from time import sleep
from celery_app import add_queue


if __name__ == '__main__':
    print('Starting publisher')
    for i in range(10000):
        queue_name = 'new_queue_{}'.format(i)
        add_queue.apply_async(args=[queue_name])
        sleep(.1)

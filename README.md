### Issue
https://github.com/celery/celery/issues/3751

### Steps to reproduce with docker compose:
1. docker-compose up --build
2. Monitor logs for `RuntimeError: Acquire on closed pool`
3. If no errors show up in 60 seconds restart the celery processes

### Steps to reproduce without docker:
1. Launch a test rabbit instance locally
2. Modify broker settings in `constants.py` to use your local rabbitmq
3. Install requirements
3. Launch celery worker 1 with:
```
celery worker -c 2 -A celery_app.app
```
4. Launch celery worker 2 with:
```
celery worker -c 2 -A celery_app.app
```
5. Launch the publisher process with:
```
python3 publisher.py
```
6. Monitor celery logs for `RuntimeError: Acquire on closed pool`
7. If no errors show up in 60 seconds restart the celery processes

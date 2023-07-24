from celery import Celery

app = Celery("digests_creator")
app.conf.broker_url = "amqp://rabbitmq:5672"


@app.task(name="test")
def test_task():
    print("task run")

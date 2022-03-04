from test_tasks.celery import app
from itertools import zip_longest, chain
from time import sleep
from celery.signals import after_task_publish

@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
	task = app.tasks.get(sender)
	backend = task.backend if task else app.backend
	backend.store_result(headers['id'], None, 'SENT')

@app.task
def string_reverse(data: str) -> str:
	sleep(2)
	return data[::-1]

@app.task
def string_double_reverse(data: str) -> str:
	sleep(5)
	return ''.join([i for i in chain(*(zip_longest(data[1::2], data[::2]))) if i])

@app.task
def string_position_repeat(data: str) -> str:
	sleep(7)
	return ''.join([data[i] * (i+1) for i in range(len(data))])	
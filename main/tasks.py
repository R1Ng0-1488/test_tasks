from test_tasks.celery import app
from itertools import zip_longest, chain
from time import sleep

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
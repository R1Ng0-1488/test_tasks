from rest_framework import serializers
from celery.result import AsyncResult

from.tasks import *


class CreateTaskSerializer(serializers.Serializer):
	CHOICES = (
		('string_reverse', 'Разворот строки.'),
		('string_double_reverse', 'Перестановку четных и нечетных символов.'),
		('string_position_repeat', 'Повтор символа в строке согласно его позиции.'),
	)
	task_type = serializers.ChoiceField(CHOICES)
	data = serializers.CharField(max_length=100, required=True,
		error_messages={'blank': 'Не все поля заполнены'})

	def save(self):
		result = globals().get(self.validated_data.get('task_type')).delay(self.validated_data.get('data'))
		return result.id


class GetTaskSerializer(serializers.Serializer):
	STATUSES = {
		'SUCCESS': 'SUCCESS',
		'SENT': 'SENT',
		'PENDING': 'DOES NOT EXIST'
 	}
 	
	task_id = serializers.CharField(max_length=100, required=True,
		error_messages={'blank': 'Не все поля заполнены'})

	def get_task(self):
		return AsyncResult(self.validated_data.get('task_id'))
		


class GetTaskStatusSerializer(GetTaskSerializer):
	
	def save(self):
		task = self.get_task()
		return self.STATUSES[task.status]


class GetTaskResultSerializer(GetTaskSerializer):
	def validate_task_id(self, value):
		task = AsyncResult(value)
		if not task.result:
			raise serializers.ValidationError(f'Статус задачи: {self.STATUSES[task.status]}')
		return value

	def save(self):
		task = self.get_task()
		return task.result
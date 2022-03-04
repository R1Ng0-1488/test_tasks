from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CreateTaskSerializer, GetTaskStatusSerializer, GetTaskResultSerializer


class BaseView(APIView):
	serializer_class = None 

	def render_response(self, data):
		return Response({'Result': True, 'task_id': data})

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			data = serializer.save()
			return self.render_response(data)
		return Response({'Result': False, 'errors': serializer.errors})


class CreateTaskView(BaseView):
	serializer_class = CreateTaskSerializer


class GetTaskStatusView(BaseView):
	serializer_class = GetTaskStatusSerializer

	def render_response(self, data):
		return Response({'Result': True, 'task_status': data})


class GetTaskResultView(BaseView):
	serializer_class = GetTaskResultSerializer

	def render_response(self, data):
		return Response({'Result': True, 'task_result': data})

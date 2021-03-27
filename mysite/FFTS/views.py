from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def new_project(request):
  if request.method == 'POST':
    data = serializers.deserialize('json', request.body)
    for deserialized_object in data:
      deserialized_object.save()
    return JsonResponse({'code': '200', 'message': 'This is a POST response!'})

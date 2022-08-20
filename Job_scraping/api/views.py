from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Job
from .serializers import JobSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def getJob(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    jobs = serializer.data
    return JsonResponse(jobs,safe=False)


@csrf_exempt
@api_view(['POST'])
def addJob(request):
    serializer = JobSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import remote.api as RemoteApi
from base.models import BaseKnowledge
from .protocol import QGProtocol

# Create your views here.
@api_view(['POST'])
def question_generation(request):
    if request.method == 'POST':
        bkd = BaseKnowledge(request.data['bkd'])
        RemoteApi.call(QGProtocol(bkd, num_case=6))
        return Response(bkd.jsonate())
    return Response({"message": "The GET method is not appropriate."})

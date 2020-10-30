from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import remote.api as RemoteApi
from base import BaseKnowledge
from .protocol import QAProtocol

# Create your views here.
@api_view(['POST'])
def answer_generation(request):
    if request.method == 'POST':
        bkd = BaseKnowledge(request.data['bkd'], 412)
        q = request.data['q']
        RemoteApi.call(QAProtocol(bkd, question=q, num_case=1))
        return Response(bkd.jsonate())
    return Response({"message": "The GET method is not appropriate."})
from django.shortcuts import render
from django.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas

import remote.api as RemoteApi
from base import BaseKnowledge
from .protocol import GQQAProtocol
from qg_interface.protocol import QGProtocol

# Create your views here.
history: list = []
@api_view(['POST'])
def answer_generation_for_generated_question(request):
    if request.method == 'POST':
        bkd = BaseKnowledge(request.data['bkd'])
        RemoteApi.call(QGProtocol(bkd))
        RemoteApi.call(GQQAProtocol(bkd))
        return Response(bkd.jsonate())
    return Response({"message": "The %s method is not appropriate." % request.method})
gqqa = answer_generation_for_generated_question

@api_view(['GET', 'DELETE'])
def gqqa_request_history(request):
    if request.method == 'DELETE':
        pass
    elif request.method == 'GET':
        history
        return HttpResponse()
    return Response({"message": "The %s method is not appropriate." % request.method})
gqqa_history = gqqa_request_history
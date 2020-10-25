from django.shortcuts import render
from django.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

import remote.api as RemoteApi
from base import BaseKnowledge
from qg_interface.protocol import QGProtocol
from .protocol import GQQAProtocol
from .statistic import GQQAStatistic

# Create your views here.
statistic = GQQAStatistic()
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
        statistic.clear()
    elif request.method == 'GET':
        return HttpResponse(statistic.to_html())
    return Response({"message": "The %s method is not appropriate." % request.method})
gqqa_history = gqqa_request_history
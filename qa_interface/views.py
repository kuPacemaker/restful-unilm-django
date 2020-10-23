from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import remote.api as RemoteApi
from base.models import BaseKnowledge
from .protocol import QAProtocol

# Create your views here.
@api_view(['POST'])
def answer_generation(request):
    if request.method == 'POST':
        bkd = BaseKnowledge(request.data['bkd'])
        q = request.data['q']
        RemoteApi.call(QAProtocol(bkd, question=q))
        return Response(bkd.jsonate())
    return Response({"message": "The GET method is not appropriate."})

@api_view(['POST'])
def answer_generation_for_generated_question(request):
    if request.method == 'POST':
        bkd = BaseKnowledge(request.data['bkd'])
        bkd.attach_question()
        bkd.replace_question()
        return Response(bkd.jsonate())
    return Response({"message": "The GET method is not appropriate."})
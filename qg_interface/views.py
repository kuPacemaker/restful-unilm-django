from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

import remote.api as RemoteApi
from base import BaseKnowledge
from .protocol import QGProtocol

# Create your views here.
@api_view(['POST'])
def question_generation(request):
    if request.method == 'POST':
        bkd = BaseKnowledge(request.data['bkd'])
        RemoteApi.call(QGProtocol(bkd))
        return Response(bkd.jsonate())
    return Response({"message": "The %s method is not appropriate." % request.method})

@api_view(['POST'])
def noun_extraction(request):
    if request.method == 'POST':
        bkd = BaseKnowledge(request.data['bkd'])
        bkd.nouns = bkd.nouns[3 + int(3 / len(bkd.passages))]
        return Response(bkd.jsonate())
    return Response({"message": "The %s method is not appropriate." % request.method})

def zero_ssl(request, filename):
    fsock = open(filename, "rb")
    return HttpResponse(fsock, content_type='text/plain')

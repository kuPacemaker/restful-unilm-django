from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

import remote.socket_api as RemoteApi
from base import BaseKnowledge
from qg_interface.protocol import QGProtocol
from .protocol import GQQAProtocol
from .statistic import GQQAHistory

from .pipeline import Pipeline, QGUnit, QAUnit

history = GQQAHistory('history.csv')
pipeline = Pipeline([QGUnit(), QAUnit()])

# Create your views here.
@api_view(['POST'])
def answer_generation_for_generated_question(request):
    if request.method == 'POST':
        bkd = BaseKnowledge(request.data['bkd'])
        bkd.passages = pipeline.start(bkd)
        return Response(bkd.jsonate())
    return Response({"message": "The %s method is not appropriate." % request.method})
gqqa = answer_generation_for_generated_question

@api_view(['GET', 'DELETE'])
def gqqa_request_history(request):
    if request.method == 'DELETE':
        history.clear()
    elif request.method == 'GET':
        history.save_csv()
        return HttpResponse(with_style(history.to_html()))
    return Response({"message": "The %s method is not appropriate." % request.method})

def with_style(html):
    return '<link rel="stylesheet" href="https://cdn.jupyter.org/notebook/5.1.0/style/style.min.css">' + html
gqqa_history = gqqa_request_history

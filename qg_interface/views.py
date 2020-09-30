from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from qg_interface.models import BaseKnowledge

# Create your views here.
@api_view(['POST', 'GET'])
def question_generation(request):
    if request.method == 'POST' || request.method == 'GET':
        text = request.data
        bkd = BaseKnowledge(text)
        bkd.attach_question()
        return Response(bkd.jsonate())
    return Response({"message": "The GET method is not appropriate."})

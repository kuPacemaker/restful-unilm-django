from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from qg_interface.models import BaseKnowledge

# Create your views here.
@api_view(['POST'])
def answer_generation(request):
    if request.method == 'POST':
        return Response({"message": "This function is not implemented yet."})
    return Response({"message": "The GET method is not appropriate."})

@api_view(['POST'])
def answer_generation_for_generated_question(request):
    if request.method == 'POST':
        bkd = BaseKnowledge(request.data['bkd'])
        bkd.attach_question()
        bkd.replace_question()
        return Response(bkd.jsonate())
    return Response({"message": "The GET method is not appropriate."})
from django.shortcuts import render
from rest_framework.decorators import api_view
from qg_interface.models import BaseKnowledge

# Create your views here.
@api_view(['POST'])
def question_generation(request):
    if request.method == 'POST':
        text = request.data
        bkd = BaseKnowledge(text)
        return Response(bkd.jsonate())
    return Response({"error": "The GET method is not appropriate."})
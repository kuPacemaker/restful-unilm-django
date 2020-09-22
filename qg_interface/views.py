from django.shortcuts import render
from rest_framework.decorators import api_view
from qg_interface.models import BaseKnowledge

# Create your views here.
@api_view(['GET','POST'])
def question_generation(request):
    if request.method == 'POST':
        text = request.data
        bkd = BaseKnowledge(text)
        return Response({"message": "success", "data": bkd.jsonate()})
    return Response({"message": "The GET method is not appropriate."})
from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes, parser_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.parsers import BaseParser
import os

class TenPerDayUserThrottle(UserRateThrottle):
    rate = '10/day'

class PlainTextParser(BaseParser):
    media_type = 'text/plain'
    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()

counter = 0

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
@throttle_classes([TenPerDayUserThrottle])
@parser_classes([PlainTextParser])
def apply_teammate(request, std_id):
    global counter
    std_file = 'ai_hackerton/' + str(std_id)

    if request.method == 'POST':
        with open(std_file, 'w') as f:
            user_input = request.data.decode('utf-8')
            f.write(user_input)
            return Response("[{}]접수 되었습니다. 곧 연락 드릴게요!".format(user_input))

    elif request.method == 'DELETE':
        try:
            os.remove(std_file)
        except:
            pass
        return Response("신청이 삭제되었습니다. 다음 기회에 뵈어요!")

    elif request.method == 'GET':
        counter += 1
        if os.path.isfile(std_file):
            return Response("당신은 지원을 접수하셨습니다. [site_page_views: {}]".format(counter))
        else:
            return Response("당신은 지원에 접수하지 않았습니다. [site_page_views: {}]".format(counter))

    return Response("The method is not allowed.")

@api_view(['GET'])
def stdid_error(request):
    return Response("학번을 입력하세요.")

@api_view(['GET'])
def stdid_value_error(request, std_id):
    return Response("학번을 바르게 입력하세요.")

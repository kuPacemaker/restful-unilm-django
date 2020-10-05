from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes, parser_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.parsers import BaseParser
from jjbcrawl.parserule import ctl_parse_rule
from jjbcrawl.crawl import Crawler
from jjbcrawl.targeturi import CtlSearchURL
import os

class TenPerDayUserThrottle(UserRateThrottle):
    rate = '10/day'

class PlainTextParser(BaseParser):
    media_type = 'text/plain'
    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()

class StudentInfo:
    url = "http://ctl.konkuk.ac.kr/ctl/ur/user_pop_list.acl?SE_FLAG=3&SCH_VALUE=201511290&SCH_KEY=I&totUSER_ID={}&EVNT_SEQ_NO=333&EVNT_DV_CD=F02&display=10&encoding=utf-8"
    @staticmethod
    def info(stdid):
        query = url.format(stdid)
        
counter = 0

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
@throttle_classes([TenPerDayUserThrottle])
@parser_classes([PlainTextParser])
def apply_teammate(request, std_id):
    global counter
    std_file = 'ai_hackerton/' + str(std_id)
    print(get_client(request))

    if request.method == 'POST':
        with open(std_file, 'w') as f:
            user_input = request.data.decode('utf-8')
            f.write(user_input)
            return Response("[{}]접수 되었습니다. 곧 연락 드릴게요!".format(user_input))

    elif request.method == 'DELETE':
        try:
            os.remove(std_file)
        except Exception as e:
            print(e)
        return Response("신청이 삭제되었습니다. 다음 기회에 뵈어요!")

    elif request.method == 'GET':
        counter += 1
        name = 'unknown'
        try:
            name = Crawler({'학번':std_id}, CtlSearchURL(), ctl_parse_rule).find_all({'이름':'td.center'}, parser='html.parser')['이름'][0]
        except Exception as e:
            print(e)
        if os.path.isfile(std_file):
            return Response("{} 님은 지원을 접수하셨습니다. [site_page_views: {}]".format(name, counter))
        else:
            return Response("{} 님은 지원에 접수하지 않았습니다. [site_page_views: {}]".format(name, counter))

    return Response("The method is not allowed.")

@api_view(['GET'])
def stdid_error(request):
    print(get_client(request))
    return Response("학번을 입력하세요.")

@api_view(['GET'])
def stdid_value_error(request, std_id):
    print(get_client(request))
    return Response("학번을 바르게 입력하세요.")

def get_client(request):
    x_f = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_f:
        ip = x_f.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

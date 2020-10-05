from .crawl import TargetURIFactory
from urllib import parse
import requests
from bs4 import BeautifulSoup

class NaverSearchURL(TargetURIFactory):
    __meta_url_format__ = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&{0}"

    def get_uri(self, key):
        query = parse.urlencode({'query': key})
        return NaverSearchURL.__meta_url_format__.format(query)


class NaverSeriesURL(TargetURIFactory):
    __series_home_url__ = "https://serieson.naver.com{0}"
    __series_search_url__ = "https://serieson.naver.com/search/search.nhn?t=all&fs=broadcasting&{0}"
    __detail_page_selector__ = "h3 > a"
    
    def get_uri(self, key):
        query = parse.urlencode({'q': key})
        series_search_url = NaverSeriesURL.__series_search_url__.format(query)
        response = requests.get(series_search_url)
        
        soup = BeautifulSoup(response.content, "html.parser")
        detail_page_url_post = soup.select_one(NaverSeriesURL.__detail_page_selector__)
        
        if detail_page_url_post is None:
            return ""

        else:
            sub_url = detail_page_url_post.attrs["href"]
            detail_page_url = NaverSeriesURL.__series_home_url__.format(sub_url)
        
        return detail_page_url


class PublicDataURL(TargetURIFactory):
    __meta_url_format__ = ""
    
    def get_uri(self, key):
        raise NotImplementedError
        
        
class CtlSearchURL(TargetURIFactory):
    __url = "http://ctl.konkuk.ac.kr/ctl/ur/user_pop_list.acl?SE_FLAG=3&SCH_VALUE={}&SCH_KEY=I&EVNT_SEQ_NO=333&EVNT_DV_CD=F02&display=10&encoding=utf-8"
    
    def get_uri(self, key):
        query = CtlSearchURL.__url.format(key)
        return query

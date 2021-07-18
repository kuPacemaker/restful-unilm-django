import requests

def call(rest):
    URL = rest.base_url()
    for payload in rest.gen_payload():
        res = requests.post(URL, json=payload)
        rest.notify_response(res)

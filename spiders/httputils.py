from aiohttp_requests import requests
import requests as reqs
async def get(url, param=None): 
    response = await requests.get(url)
    ret = await response.text()
    return ret

async def post(url, data=None): 
    response = await requests.post(url, data=data)
    ret = await response.text()
    return ret

async def image(url):
    # lazy way ...
    while(True):
        try:
            response = await requests.get(url)
            return response.content()
        except:
            pass
    
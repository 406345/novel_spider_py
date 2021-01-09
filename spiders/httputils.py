from aiohttp_requests import requests

async def get(url, param=None):
    # data = {
    #         "csrfmiddlewaretoken":"qGLEc713lNum7u0M1ddsXrsqb9WPEr7nuErl9M6XayHfnx2D1t80cLETVuF6MYwr",
    #         "username":"admin",
    #         "password":"123456",
    #         "next":"%2Fadmin%2F"
    #     }
    response = await requests.get(url)
    ret = await response.text()
    return ret

async def post(url, data=None):
    # data = {
    #         "csrfmiddlewaretoken":"qGLEc713lNum7u0M1ddsXrsqb9WPEr7nuErl9M6XayHfnx2D1t80cLETVuF6MYwr",
    #         "username":"admin",
    #         "password":"123456",
    #         "next":"%2Fadmin%2F"
    #     }
    response = await requests.post(url, data=data)
    ret = await response.text()
    return ret

def image(url):
    # data = {
    #         "csrfmiddlewaretoken":"qGLEc713lNum7u0M1ddsXrsqb9WPEr7nuErl9M6XayHfnx2D1t80cLETVuF6MYwr",
    #         "username":"admin",
    #         "password":"123456",
    #         "next":"%2Fadmin%2F"
    #     }
    response = requests.get(url)
    return response.content

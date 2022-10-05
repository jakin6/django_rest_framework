import requests

headers={
    'Authorization':'Bearer ab2e424034660fc9910ef7055e5af062bcc07b40'
}
endpoint="http://localhost:8000/api/products/"

data = {
    "title":"This field is done",
    "price":32.99
}
get_response=requests.post(endpoint,json=data,headers=headers) #HTTP Request
print(get_response.json())
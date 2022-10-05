import requests

product_id=input("What is the product id you want to use ?\n")
try:
    product_id=int(product_id)
except:
    product_id=None
    print(f'{product_id} not a valid id')

if product_id:
    endpoint= f"http://localhost:8000/api/products/{product_id}/delete/"
    # http request
    get_response=requests.delete(endpoint,json={"title":"Abc123","content":"Hello world"}) 
    print(get_response.status_code,
    get_response.status_code==204)
    print(product_id)






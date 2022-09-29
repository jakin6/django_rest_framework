from django.forms.models import model_to_dict
from products.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view


from products.serializers import ProductSerializer

# @api_view(["GET"])
# def api_home(request,*args,**kwargs):
#     """"
#     DRF API View
#     """
#     instance=Product.objects.all().order_by("?").first()
#     data={}
#     if instance:
#         data =ProductSerializer(instance).data
#     return Response(data)


@api_view(["POST"])
def api_home(request,*args,**kwargs):
    """"
    DRF API View
    """
 
    serializer=ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        print(instance)
        return Response(serializer.data)
    return Response({"Invalid":"not good data"},status=400)
  
  
  
  
   
    # serializer=ProductSerializer(data=request.data)
    # if serializer.is_valid(raise_exception=True):
    #     instance = serializer.save()
    #     print(instance)
    #     return Response(serializer.data)
    # return Response({"Invalid":"not good data"},status=400)
  
    # print(request.GET)
    # print(request.POST)
    # body=request.body #byte string of  Json data
    # data={}
    # try:
    #     data=json.loads(body) #json data to python dict
    # except:
    #     pass
    # print(data)
    # print(request.headers)
    # data['params']=dict(request.GET)
    # data['header']=dict(request.headers)
    # data['content_type']=request.content_type

     # data['id']=model_data.id
        # data['title']=model_data.title
        # data['content']=model_data.content
        # data['price']=model_data.price
        #model instance(model_data)
        #turn a Python dict
        #return JsoN to my client
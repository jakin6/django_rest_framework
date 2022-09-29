from ast import Or
from urllib import request
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title=serializer.validated_data.get('title')
        content=serializer.validated_data.get('content')

        if content is None:
            content=title
        serializer.save(content=content)

product_create_view=ProductCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    # lookup_field = 'pk'

product_detail_view=ProductDetailAPIView.as_view()

"""
class ProductListAPIView(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title=serializer.validated_data.get('title')
        content=serializer.validated_data.get('content') or None

        if content is None:
            content=title
        serializer.save(content=content)

product_list_view=ProductDetailAPIView.as_view()
"""

@api_view(['GET','POST'])
def product_alt_view(request,pk=None,*args,**kwargs):
    method=request.method

    if method == "GET":
        if pk is not None:
            # detail view
            """
            # queryset=Product.objects.filter(pk=pk)
            # if not queryset.exist():
            # raise Http404
            """
            obj=get_object_or_404(Product,pk=pk) 
            data =ProductSerializer(obj,many=False).data
            return Response(data)

        #list view
        queryset=Product.objects.all()
        data=ProductSerializer(queryset,many=True).data
        return Response(data)

    if method == 'POST':
        # request data
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title=serializer.validated_data.get('title')
            content=serializer.validated_data.get('content') or None
            if content is None:
                content=title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"Invalid":"not good data"},status=400)


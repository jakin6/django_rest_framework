from rest_framework import authentication,generics,mixins,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.authentication  import TokenAuthentication
from api.mixins import StaffEditorPermissionMixin

from .models import Product
from  api.permissions import IsStaffPermission
from .serializers import ProductSerializer

class ProductCreateAPIView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
    # authentication_classes=[authentication.SessionAuthentication,
    #     TokenAuthentication]
    # permission_classes=[permissions.DjangoModelPermissions] 
    permission_classes=[permissions.IsAdminUser,IsStaffPermission]

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


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field = 'pk'

    def perform_update(self,serializer):
        instance =serializer.save()
        if not instance.content:
            instance.content=instance.title
            #   

product_update_view=ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field = 'pk'
    permission_classes=[permissions.IsAdminUser,IsStaffPermission]


    def perform_destroy(self,instance):
        # instance
        super().perform_destroy(instance)

product_destroy_view=ProductDestroyAPIView.as_view()

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

product_list_view=ProductListAPIView.as_view()


# Using mixins in view
class ProductMixinView(
mixins.CreateModelMixin,
mixins.ListModelMixin,
mixins.RetrieveModelMixin,
generics.GenericAPIView,
):

    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'

    def get(self,request,*args,**kwargs):
        print(args,kwargs)
        pk=kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request,*args,**kwargs)
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def perform_create(self, serializer):

        title=serializer.validated_data.get('title')
        content=serializer.validated_data.get('content') or None

        if content is None:
            content="This is single view doing cool stuff"
        serializer.save(content=content)

product_mixin_view=ProductMixinView.as_view()

""" 
#This function shows how to use one function for all  crud even though is 
#not a good practice 
@api_view(['GET','POST'])
def product_alt_view(request,pk=None,*args,**kwargs):
    method=request.method

    if method == "GET":
        if pk is not None:
            # detail view
            # queryset=Product.objects.filter(pk=pk)
            # if not queryset.exist():
            # raise Http404
            
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
"""

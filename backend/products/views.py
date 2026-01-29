# Create your views here.


from .seralizers import ProductSerializer


def product(request):
    serializer = ProductSerializer(data=request.data)
    

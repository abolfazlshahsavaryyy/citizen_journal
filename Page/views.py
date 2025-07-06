# myapp/views.py

from rest_framework.views import APIView
from .models import Page
from .serelizers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
class PageListCreateView(APIView):
    """
    GET: List all pages
    POST: Create a new page
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    def get (self,request):
        pages=Page.objects.all().order_by('follower_count')
        serelizer=PageSerializer(pages,many=True)
        return Response(serelizer.data)
    
    def post(self,request):
        
        serelizer=PageCreateSerializer(data=request.data)
        if(serelizer.is_valid()):
            serelizer.save()
            return Response(serelizer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serelizer.errors+' request error',status=status.HTTP_400_BAD_REQUEST)


# class PageDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     GET: Retrieve a specific page by ID
#     PUT: Update a page (full update)
#     DELETE: Delete a page
#     """
#     queryset = Page.objects.all()
#     serializer_class = PageSerializer

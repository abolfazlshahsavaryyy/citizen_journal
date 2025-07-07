# myapp/views.py

from rest_framework.views import APIView
from ..models import Page
from Page.serializer.page_serializer import *
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


class PageDetailView(APIView):
    """
    GET: Retrieve a specific page by ID
    PUT: Update a page (full update)
    DELETE: Delete a page
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    def _get_page_by_pk(self, pk):
        try:
            return Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            raise Exception("Page not found")

    def get (self,request,pk):
        try:
            page=self._get_page_by_pk(pk)
            page_serializer=PageDetailseSerializer(page)
            return Response(data=page_serializer.data,status=status.HTTP_200_OK)
        except:
            page_serializer=PageDetailseSerializer(page)
            return Response(data=page_serializer.errors,status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk):
        try:
            post = self._get_page_by_pk(pk)
            serializer = PostUpdateSerializer(post, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Request not in correct format', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,pk):
        try:
            post=self._get_page_by_pk(pk)
            post.delete()
            return Response({'detail': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
# myapp/views.py

from rest_framework.views import APIView
from Page.models.Page import Page
from Page.serializer.page_serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from drf_yasg.utils import swagger_auto_schema
from Page.services.page_service import *
from rest_framework.throttling import ScopedRateThrottle
class PageListCreateView(APIView):
    """
    GET: List all pages
    POST: Create a new page
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    
    def get(self, request):
        pages = Page.objects.select_related('user').order_by('follower_count')
        serializer = PageSerializer(pages, many=True)
        return Response(serializer.data)

    
    permission_classes = [IsAuthenticated]
    throttle_scope = 'create_page'  # use the key from settings
    throttle_classes = [ScopedRateThrottle]
    @swagger_auto_schema(
        request_body=PageCreateSerializer,
        responses={201: PageCreateSerializer}
    )
    def post(self, request):
        serializer = PageCreateSerializer(data=request.data)
        if serializer.is_valid():
            page = create_page(request.user, serializer.validated_data)
            response_serializer = PageCreateSerializer(page)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageDetailView(APIView):
    """
    GET: Retrieve a specific page by ID
    PUT: Update a page (full update)
    DELETE: Delete a page
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    def _get_page_by_pk(self, pk):
        return Page.objects.get(pk=pk)  # Let it raise Page.DoesNotExist naturally


    def get(self, request, pk):
        try:
            page = self._get_page_by_pk(pk)
        except Page.DoesNotExist:
            return Response({'error': 'Page not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        # If no exception, serialize and return
        page_serializer = PageDetailseSerializer(page)
        return Response(data=page_serializer.data, status=status.HTTP_200_OK)

        
    @swagger_auto_schema(
        request_body=PostUpdateSerializer,
        responses={201: PostUpdateSerializer}
    )
    def put(self, request, pk):
        try:
            page = self._get_page_by_pk(pk)

            if page.user != request.user:
                return Response(
                    {"error": "You do not have permission to edit this page."},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = PostUpdateSerializer(page, data=request.data)
            if serializer.is_valid():
                updated_page = update_page(page, serializer.validated_data)
                response_serializer = PostUpdateSerializer(updated_page)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Page.DoesNotExist:
            return Response({'error': 'Page not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': 'Request not in correct format', 'details': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            page = self._get_page_by_pk(pk)

            if page.user != request.user:
                return Response(
                    {"error": "You do not have permission to delete this page."},
                    status=status.HTTP_403_FORBIDDEN
                )

            delete_page(page)
            return Response({'detail': 'Page deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Page.DoesNotExist:
            return Response({'error': 'Page not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': 'Request not in correct format', 'details': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
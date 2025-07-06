# myapp/views.py

from rest_framework import generics
from .models import Page
from .serelizers import PageSerializer

class PageListCreateView(generics.ListCreateAPIView):
    """
    GET: List all pages
    POST: Create a new page
    """
    queryset = Page.objects.all().order_by('-follower_count')
    serializer_class = PageSerializer


class PageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific page by ID
    PUT: Update a page (full update)
    DELETE: Delete a page
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer

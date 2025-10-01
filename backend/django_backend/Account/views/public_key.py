# Account/views/public_key_view.py
from rest_framework.views import APIView
from django.http import HttpResponse

class PublicKeyView(APIView):
    # Make this endpoint public
    authentication_classes = []  # No auth
    permission_classes = []      # Public access

    def get(self, request):
        """
        Return the JWT public key as plain text.
        """
        with open("config/jwtRS256.key.pub", "r") as f:
            public_key = f.read()
        return HttpResponse(public_key, content_type="text/plain")

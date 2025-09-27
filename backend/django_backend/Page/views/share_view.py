from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Page.grpc import share_news_pb2, share_news_pb2_grpc
import grpc
from Page.serializer.share_serializer import *

channel = grpc.insecure_channel("sharenewsgrpc:8080")
stub = share_news_pb2_grpc.ShareNewsServiceStub(channel)


@swagger_auto_schema(
    method='get',
    responses={200: GetShareNewsByUserResponseSerializer}
)
@api_view(['GET'])
def get_share_news_by_user(request):
    user_id = request.user.id
    grpc_request = share_news_pb2.GetShareNewsByUserRequest(userId=int(user_id))
    response = stub.GetShareNewsByUser(grpc_request)

    return Response({
        "items": [
            {
                "id": item.id,
                "userIdSender": item.userIdSender,
                "newsId": item.newsId,
                "userIdReceiver": item.userIdReceiver,
                "content": item.content,
                "createdAt": item.createdAt
            } for item in response.items
        ]
    })


@swagger_auto_schema(
    method='post',
    request_body=AddShareNewsRequestSerializer,
    responses={200: AddShareNewsResponseSerializer}
)
@api_view(['POST'])
def add_share_news(request):
    serializer = AddShareNewsRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    grpc_request = share_news_pb2.AddShareNewsRequest(
        userIdSender=request.user.id,
        newsId=data["newsId"],
        userIdReceiver=data["userIdReceiver"],
        content=data.get("content", "")
    )
    response = stub.AddShareNews(grpc_request)

    return Response({
        "item": {
            "id": response.item.id,
            "userIdSender": response.item.userIdSender,
            "newsId": response.item.newsId,
            "userIdReceiver": response.item.userIdReceiver,
            "content": response.item.content,
            "createdAt": response.item.createdAt,
        }
    })


@swagger_auto_schema(
    method='post',
    request_body=RemoveShareNewsRequestSerializer,
    responses={200: RemoveShareNewsResponseSerializer}
)
@api_view(['POST'])
def remove_share_news(request):
    serializer = RemoveShareNewsRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    
    grpc_request = share_news_pb2.RemoveShareNewsRequest(shareNewsId=data["shareNewsId"])
    response = stub.RemoveShareNews(grpc_request)

    return Response({
        "shareNewsId": response.shareNewsId
    })

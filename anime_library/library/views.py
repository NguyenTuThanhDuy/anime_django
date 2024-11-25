from datetime import datetime
import re

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from library.controllers.channel_controller import ChannelController
from library.serializers import ChannelIDsSerializer, ChannelSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_channel_by_id_api(request: Request, channel_id: str):
    try:
        res = ChannelController().get_channel_by_id(channel_id)
        res = ChannelSerializer(res)
        return JsonResponse({"data": res.data}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return JsonResponse({"msg": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"msg": "Error"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_channels_by_ids_api(request: Request):
    # Validate the input using the serializer
    serializer = ChannelIDsSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(
            {"msg": "Invalid input", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Extract validated data
    channel_ids = serializer.validated_data['channel_ids']
    if not channel_ids:
        return JsonResponse({"msg": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        res = ChannelController().get_list_channels_by_ids(channel_ids)
        return JsonResponse({"data": list(res)}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return JsonResponse({"msg": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError:
        return JsonResponse({"msg": "Invalid datatype"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as e:
        return JsonResponse({"msg": "Error"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_channel(request: Request):
    # Access the authenticated user
    authenticated_user = request.user

    # Include the user in the serializer data
    data = request.data.copy()
    data['channel_owner'] = authenticated_user.id
    user_channel = ChannelController().get_channel_by_user_id(authenticated_user.id)
    if user_channel:
        return JsonResponse({"msg": "User has channel already, cannot create more"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the data with the serializer
    serializer = ChannelSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse(
            {"msg": "Invalid input", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Save the channel with the authenticated user
    channel = serializer.save()

    # Serialize the created channel
    serialized_channel = ChannelSerializer(channel)

    return JsonResponse(
        {"msg": "Success", "data": serialized_channel.data},
        status=status.HTTP_201_CREATED
    )

@api_view(['PUT', 'POST'])
def edit_channel(request: Request, channel_id: str):
    data = request.data
    try:
        user_channel = ChannelController().get_channel_by_id(channel_id)
    except ObjectDoesNotExist:
        return JsonResponse({"msg": "Channel not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChannelSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse(
            {"msg": "Invalid input", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    channel = serializer.update(user_channel, serializer.data)

    # Serialize the created channel
    serialized_channel = ChannelSerializer(channel)

    return JsonResponse(
        {"msg": "Success", "data": serialized_channel.data},
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_videos(request: Request):
    query_params = request.query_params
    limit = int(query_params.get("limit", 20))
    offset = int(query_params.get("offset", 0))

    query_title = query_params.get("title")
    data = [
        {
            "id": "1",
            "title": "CSS Anchor Is The Best New CSS Feature Since Flexbox",
            "channel": {
                "name": "Web Dev Simplified",
                "id": "WebDevSimplified",
                "profileUrl": "https:yt3.ggpht.com/ytc/APkrFKZWeMCsx4Q9e_Hm6nhOOUQ3fv96QGUXiMr1-pPP=s48-c-k-c0x00ffffff-no-rj",
            },
            "views": 222536,
            "postedAt": datetime.today().strftime("%d-%m-%Y"),
            "duration": 938,
            "thumbnailUrl": "https:i.ytimg.com/vi/B4Y9Ed4lLAI/maxresdefault.jpg",
            "videoUrl": "https:storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        },
        {
            "id": "2",
            "title": "NEW Way To Create Variables In JavaScript",
            "channel": {
                "name": "Web Dev Simplified",
                "id": "WebDevSimplified",
                "profileUrl": "https:yt3.ggpht.com/ytc/APkrFKZWeMCsx4Q9e_Hm6nhOOUQ3fv96QGUXiMr1-pPP=s48-c-k-c0x00ffffff-no-rj",
            },
            "views": 257136,
            "postedAt": datetime.today().strftime("%d-%m-%Y"),
            "duration": 732,
            "thumbnailUrl": "https:i.ytimg.com/vi/d6a8RymS1zI/maxresdefault.jpg",
            "videoUrl": "https:storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        },
        {
            "id": "3",
            "title": "Front-end developer takes on a CSS battle",
            "channel": {
                "name": "Kevin Powell",
                "id": "KevinPowell",
                "profileUrl": "https:yt3.ggpht.com/ytc/APkrFKa6XiLa13mMVPzkmmTBcgNPjjqCGPrY86KfJFmf5w=s48-c-k-c0x00ffffff-no-rj",
            },
            "views": 1232300,
            "postedAt": datetime.today().strftime("%d-%m-%Y"),
            "duration": 120,
            "thumbnailUrl": "https:i.ytimg.com/vi/eYPyIq5Y3Rk/maxresdefault.jpg",
            "videoUrl": "https:storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        },
        {
            "id": "4",
            "title": "Quick guide to CSS focus states",
            "channel": {
                "name": "Kevin Powell",
                "id": "KevinPowell",
                "profileUrl": "https:yt3.ggpht.com/ytc/APkrFKa6XiLa13mMVPzkmmTBcgNPjjqCGPrY86KfJFmf5w=s48-c-k-c0x00ffffff-no-rj",
            },
            "views": 112,
            "postedAt": datetime.today().strftime("%d-%m-%Y"),
            "duration": 4343,
            "thumbnailUrl": "https:i.ytimg.com/vi/apdD69J4bEc/maxresdefault.jpg",
            "videoUrl": "https:storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        },
        {
            "id": "5",
            "title": "I Cannot Believe React Made A Hook For This",
            "channel": {
                "name": "Web Dev Simplified",
                "id": "WebDevSimplified",
                "profileUrl": "https:yt3.ggpht.com/ytc/APkrFKZWeMCsx4Q9e_Hm6nhOOUQ3fv96QGUXiMr1-pPP=s48-c-k-c0x00ffffff-no-rj",
            },
            "views": 42345,
            "postedAt": datetime.today().strftime("%d-%m-%Y"),
            "duration": 1000,
            "thumbnailUrl": "https:i.ytimg.com/vi/M3mGY0pgFk0/maxresdefault.jpg",
            "videoUrl": "https:storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        },
        {
            "id": "6",
            "title": "I Got Laid Off...",
            "channel": {
                "name": "Caleb Curry",
                "id": "CalebCurry",
                "profileUrl": "https:yt3.googleusercontent.com/ytc/APkrFKbpSojje_-tkBQecNtFuPdSCrg3ZT0FhaYjln9k0g=s176-c-k-c0x00ffffff-no-rj",
            },
            "views": 10340,
            "postedAt": datetime.today().strftime("%d-%m-%Y"),
            "duration": 54,
            "thumbnailUrl": "https:i.ytimg.com/vi/i2JVQdLnkAY/maxresdefault.jpg",
            "videoUrl": "https:storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        },
        {
            "id": "7",
            "title": "Tails OS in 100 Seconds",
            "channel": {
                "name": "Fireship",
                "id": "Fireship",
                "profileUrl": "https:yt3.googleusercontent.com/ytc/APkrFKb--NH6RwAGHYsD3KfxX-SAgWgIHrjR5E4Jb5SDSQ=s176-c-k-c0x00ffffff-no-rj",
            },
            "views": 10323340,
            "postedAt": datetime.today().strftime("%d-%m-%Y"),
            "duration": 100,
            "thumbnailUrl": "https:i.ytimg.com/vi/mVKAyw0xqxw/maxresdefault.jpg",
            "videoUrl": "https:storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        },
        {
            "id": "8",
            "title": "Zig in 100 Seconds",
            "channel": {
                "name": "Fireship",
                "id": "Fireship",
                "profileUrl": "https:yt3.googleusercontent.com/ytc/APkrFKb--NH6RwAGHYsD3KfxX-SAgWgIHrjR5E4Jb5SDSQ=s176-c-k-c0x00ffffff-no-rj",
            },
            "views": 20323340,
            "postedAt": datetime.today().strftime("%d-%m-%Y"),
            "duration": 105,
            "thumbnailUrl": "https:i.ytimg.com/vi/kxT8-C1vmd4/maxresdefault.jpg",
            "videoUrl": "https:storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        },
    ]
    if not query_title:
        return JsonResponse({'msg': 'Get videos successfully', 'videos': data[offset: limit + offset], 'total': len(data)}, status=status.HTTP_200_OK)
    pattern = f".*({query_title}.*)"

    response_data = [x for x in data if re.search(pattern, x['title'], re.IGNORECASE)]
    return JsonResponse({'msg': 'Get videos successfully', 'videos': response_data[offset: limit + offset]}, status=status.HTTP_200_OK)

from datetime import datetime
import re

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.


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
        return Response({'msg': 'Get videos successfully', 'videos': data[offset: limit + offset], 'total': len(data)}, status=status.HTTP_200_OK)
    pattern = f".*({query_title}.*)"

    response_data = [x for x in data if re.search(pattern, x['title'], re.IGNORECASE)]
    return Response({'msg': 'Get videos successfully', 'videos': response_data[offset: limit + offset]}, status=status.HTTP_200_OK)

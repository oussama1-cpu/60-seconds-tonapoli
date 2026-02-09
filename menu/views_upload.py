from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from datetime import datetime

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    """
    Upload image from Flutter app
    Category can be: 'menu_item', 'ingredient', 'category', 'profile'
    """
    try:
        if 'image' not in request.FILES:
            return Response(
                {'error': 'No image file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        category = request.data.get('category', 'general')
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_extension = os.path.splitext(image_file.name)[1]
        filename = f"{category}_{timestamp}{file_extension}"
        
        # Save file
        file_path = f'{category}s/{filename}'  # e.g., 'menu_items/menu_item_20241113_123456.jpg'
        path = default_storage.save(file_path, ContentFile(image_file.read()))
        
        # Return the URL
        image_url = request.build_absolute_uri(default_storage.url(path))
        
        return Response({
            'success': True,
            'image_url': image_url,
            'file_path': path
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

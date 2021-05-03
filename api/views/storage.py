import datetime

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from google.cloud import storage

from vounty_backend.settings import GS_CREDENTIALS


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def storage_url(request):
    date = datetime.datetime.utcnow()
    expiration = date + datetime.timedelta(minutes=10)
    client = storage.Client(credentials=GS_CREDENTIALS)
    date = datetime.datetime.now(datetime.timezone.utc)

    bucket = client.bucket('vounty-storage')
    blob = bucket.blob('image/' + date.isoformat())
    getter = blob.generate_signed_url(expiration=expiration, method='GET', version='v4')
    setter = blob.generate_signed_url(expiration=expiration, method='PUT', version='v4')

    return JsonResponse({'getter': getter, 'setter': setter})

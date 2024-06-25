from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tt.celery_tasks import send_reqs

@api_view(['GET'])
def test_endpoint(request):
    try:
        send_reqs.delay()
        return Response(status=status.HTTP_200_OK, data={"ok": True})
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"ok": False, "message": "Произошла непредвиденная ошибка."})

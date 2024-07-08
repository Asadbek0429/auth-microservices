from datetime import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Services, SSOToken


class AuthViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get token",
        operation_summary="Get token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id', 'name', 'secret_key'],
            properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER, title='Service id'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, title='Service name'),
                        'secret_key': openapi.Schema(type=openapi.TYPE_STRING, title='secret_key')}
        ),
        responses={200: 'Token'},
        tags=['Service']
    )
    def login(self, request, *args, **kwargs):
        data = request.data
        service = Services.objects.filter(id=data.get('id'), name=data.get('name'),
                                          secret_key=data.get('secret_key')).first()
        if not service:
            return Response(data={'error': 'Service name or secret_key is incorrect', 'ok': False},
                            status=status.HTTP_400_BAD_REQUEST)
        token = SSOToken.objects.create(service=service)
        token.save()
        return Response(data={'token': token.token, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Check token",
        operation_summary="Check token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['token'],
            properties={'token': openapi.Schema(type=openapi.TYPE_STRING, title='Token')}
        ),
        responses={200: 'Token is correct'},
        tags=['Service']
    )
    def check(self, request, *args, **kwargs):
        data = request.data
        service = SSOToken.objects.filter(token=data.get('token'), deleted_at__isnull=True).first()
        if not service:
            return Response(data={'error': 'Token is incorrect', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        service.deleted_at = datetime.now()
        service.save(update_fields=['deleted_at'])
        return Response(data={'message': 'Token is correct', 'ok': True}, status=status.HTTP_200_OK)

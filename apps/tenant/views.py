from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers
from apps.tenant.models import Tenant
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant
        fields = ('name', 'is_active',)


class TenantViewSet(
    GenericViewSet
):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    required_alternate_scopes = {
        'GET': [['read']],
    }

    @action(
        url_path='',
        detail=False,
        methods=['GET'],
        serializer_class=TenantSerializer
    )
    def current_tennant(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(instance=request.user)
        return Response(data=serializer.data)

from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import serializers
from apps.tenant.models import Tenant
from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements
from oauth2_provider.contrib.rest_framework.authentication import \
    OAuth2Authentication


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant
        fields = ('name', 'is_active',)


class TenantViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {
        'GET': [['read']],
    }

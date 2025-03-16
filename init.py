from oauth2_provider.models import Application
from django.contrib.auth import get_user_model

Tenant = get_user_model()

tenant = Tenant.objects.filter(name='admin').first()
if not tenant:
    tenant = Tenant.objects.create_superuser(
        'admin', 'admin', **{}
    )
    print(f"[+] Initialized Tenant: {tenant.name}")

app, _ = Application.objects.update_or_create(
    name="POC Authorization",
    defaults={
        'client_id': "poc-authorization",
        'client_secret': "super-secret",
        'client_type': Application.CLIENT_CONFIDENTIAL,
        'authorization_grant_type': Application.GRANT_AUTHORIZATION_CODE,
        'redirect_uris': "http://127.0.0.1:5000/callback/",
        'user': tenant,
        'algorithm': Application.HS256_ALGORITHM
    }
)

app, _ = Application.objects.update_or_create(
    name="POC Client Credential",
    defaults={
        'client_id': "poc-client-credential",
        'client_secret': "super-secret",
        'client_type': Application.CLIENT_CONFIDENTIAL,
        'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS,
        # 'redirect_uris': "http://127.0.0.1:5000/callback/",
        'user': tenant,
        # 'algorithm': Application.HS256_ALGORITHM
    }
)

print(f"[+] Initialized application: {app.name}, Client ID: {app.client_id}")

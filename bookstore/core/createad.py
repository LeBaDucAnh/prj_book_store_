from django.contrib.auth import get_user_model

User = get_user_model()

admin_user = User.objects.create_superuser(email='admin1@gmail.com', password='ducanh501')
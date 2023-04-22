from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    password = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def get_fullname(cus_id):
        return Customer.objects.filter(id = cus_id).values('fullname')

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

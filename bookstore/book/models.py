from django.db import models
from bookstore.const import BOOK_STATUS
from category.models import Category
from author.models import Author

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    book_name = models.CharField(max_length=255, blank=True)
    dimensions = models.CharField(max_length=255, blank=True)
    pages = models.IntegerField(blank=True)
    publication_date = models.DateField(blank=True)
    language  = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    unit_price = models.IntegerField(blank=True)
    status = models.CharField(choices=BOOK_STATUS, default='IN STOCK', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qty = models.IntegerField(blank=True)
    total_qty = models.IntegerField(blank=True)
    image = models.ImageField(upload_to='books/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    
    @staticmethod
    def get_books_by_id(ids):
        return Book.objects.filter (id__in=ids)
    
    @staticmethod
    def get_all_books():
        return Book.objects.all()

    @staticmethod
    def get_all_books_by_categoryid(category_id):
        if category_id:
            return Book.objects.filter (category=category_id)
        else:
            return Book.get_all_books()
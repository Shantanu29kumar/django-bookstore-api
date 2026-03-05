from django.db import models

# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=200)
    book_id = models.CharField(max_length=50,unique=True)
    lender_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    date_given = models.DateField(null=True,blank=True)
    date_returned = models.DateField(null=True,blank=True)
    is_returned = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_name
    
    

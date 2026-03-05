from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    book_name = models.CharField(max_length=200)

    book_id = models.CharField(max_length=50, unique=True)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_name


class Borrower(models.Model):
    name = models.CharField(max_length=200)

    phone_number = models.CharField(max_length=15)

    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class LoanRecord(models.Model):

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    borrower = models.ForeignKey(
        Borrower,
        on_delete=models.CASCADE
    )

    date_given = models.DateField()

    date_returned = models.DateField(null=True, blank=True)

    is_returned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.book_name} borrowed by {self.borrower.name}"
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Book, Author, Borrower, LoanRecord


# ─────────────────────────────────────────────
#  AUTHOR VIEWS
# ─────────────────────────────────────────────

@csrf_exempt
def create_author(request):
    """POST /authors/create/  – create a new author"""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    try:
        data = json.loads(request.body)
        name = data.get("name")
        if not name:
            return JsonResponse({"error": "name is required"}, status=400)
        author = Author.objects.create(
            name=name,
            email=data.get("email", ""),
            bio=data.get("bio", ""),
        )
        return JsonResponse({
            "message": "Author created successfully",
            "author_id": author.id,
            "name": author.name,
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_authors(request):
    """GET /authors/  – list all authors"""
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)
    authors = Author.objects.all().values("id", "name", "email", "bio")
    return JsonResponse(list(authors), safe=False)


def get_author(request, author_id):
    """GET /authors/<id>/  – get a single author with their books"""
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return JsonResponse({"error": "Author not found"}, status=404)
    books = list(author.books.values("book_id", "book_name", "created_at"))
    return JsonResponse({
        "id": author.id,
        "name": author.name,
        "email": author.email,
        "bio": author.bio,
        "books": books,
    })


# ─────────────────────────────────────────────
#  BOOK VIEWS
# ─────────────────────────────────────────────

@csrf_exempt
def create_book(request):
    """
    POST /books/create/
    Body: { "book_name": "...", "book_id": "...", "author_id": 1 }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    try:
        data = json.loads(request.body)
        book_name = data.get("book_name")
        book_id   = data.get("book_id")
        author_id = data.get("author_id")
        if not book_name or not book_id or not author_id:
            return JsonResponse(
                {"error": "book_name, book_id, and author_id are required"},
                status=400,
            )
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return JsonResponse({"error": "Author not found"}, status=404)
        book = Book.objects.create(
            book_name=book_name,
            book_id=book_id,
            author=author,
        )
        return JsonResponse({
            "message": "Book created successfully",
            "book_id": book.book_id,
            "book_name": book.book_name,
            "author": author.name,
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_books(request):
    """GET /books/  – list all books with author info"""
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)
    books = Book.objects.select_related("author").all()
    books_list = [
        {
            "book_id": b.book_id,
            "book_name": b.book_name,
            "author_id": b.author.id,
            "author_name": b.author.name,
            "created_at": b.created_at,
        }
        for b in books
    ]
    return JsonResponse(books_list, safe=False)


@require_http_methods(["GET"])
def get_book(request, book_id):
    """GET /books/<book_id>/  – get a single book"""
    try:
        book = Book.objects.select_related("author").get(book_id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)
    return JsonResponse({
        "book_id": book.book_id,
        "book_name": book.book_name,
        "author_id": book.author.id,
        "author_name": book.author.name,
        "created_at": book.created_at,
    })


@csrf_exempt
@require_http_methods(["PUT"])
def update_book(request, book_id):
    """PUT /books/update/<book_id>/  – update book_name or author"""
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    book.book_name = data.get("book_name", book.book_name)
    new_author_id = data.get("author_id")
    if new_author_id:
        try:
            book.author = Author.objects.get(id=new_author_id)
        except Author.DoesNotExist:
            return JsonResponse({"error": "Author not found"}, status=404)
    book.save()
    return JsonResponse({"message": "Book updated successfully"})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_book(request, book_id):
    """DELETE /books/delete/<book_id>/"""
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)
    book.delete()
    return JsonResponse({"message": "Book deleted successfully"})


# ─────────────────────────────────────────────
#  BORROWER VIEWS
# ─────────────────────────────────────────────

@csrf_exempt
def create_borrower(request):
    """
    POST /borrowers/create/
    Body: { "name": "...", "phone_number": "...", "email": "..." }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    try:
        data = json.loads(request.body)
        name         = data.get("name")
        phone_number = data.get("phone_number")
        if not name or not phone_number:
            return JsonResponse(
                {"error": "name and phone_number are required"},
                status=400,
            )
        borrower = Borrower.objects.create(
            name=name,
            phone_number=phone_number,
            email=data.get("email", ""),
        )
        return JsonResponse({
            "message": "Borrower created successfully",
            "borrower_id": borrower.id,
            "name": borrower.name,
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_borrowers(request):
    """GET /borrowers/  – list all borrowers"""
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)
    borrowers = Borrower.objects.all().values("id", "name", "phone_number", "email")
    return JsonResponse(list(borrowers), safe=False)


# ─────────────────────────────────────────────
#  LOAN RECORD VIEWS
# ─────────────────────────────────────────────

@csrf_exempt
def create_loan(request):
    """
    POST /loans/create/
    Body: {
        "book_id": "B001",
        "borrower_id": 1,
        "date_given": "2025-01-01",
        "date_returned": "2025-01-15"   (optional)
    }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    try:
        data = json.loads(request.body)
        book_id     = data.get("book_id")
        borrower_id = data.get("borrower_id")
        date_given  = data.get("date_given")
        if not book_id or not borrower_id or not date_given:
            return JsonResponse(
                {"error": "book_id, borrower_id, and date_given are required"},
                status=400,
            )
        try:
            book = Book.objects.get(book_id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)
        try:
            borrower = Borrower.objects.get(id=borrower_id)
        except Borrower.DoesNotExist:
            return JsonResponse({"error": "Borrower not found"}, status=404)
        loan = LoanRecord.objects.create(
            book=book,
            borrower=borrower,
            date_given=date_given,
            date_returned=data.get("date_returned"),
            is_returned=data.get("is_returned", False),
        )
        return JsonResponse({
            "message": "Loan record created successfully",
            "loan_id": loan.id,
            "book": book.book_name,
            "borrower": borrower.name,
            "date_given": str(loan.date_given),
            "is_returned": loan.is_returned,
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_loans(request):
    """GET /loans/  – list all loan records"""
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)
    loans = LoanRecord.objects.select_related("book", "borrower").all()
    loans_list = [
        {
            "loan_id": loan.id,
            "book_id": loan.book.book_id,
            "book_name": loan.book.book_name,
            "borrower_id": loan.borrower.id,
            "borrower_name": loan.borrower.name,
            "phone_number": loan.borrower.phone_number,
            "date_given": str(loan.date_given),
            "date_returned": str(loan.date_returned) if loan.date_returned else None,
            "is_returned": loan.is_returned,
        }
        for loan in loans
    ]
    return JsonResponse(loans_list, safe=False)


@csrf_exempt
def update_loan(request, loan_id):
    """
    PUT /loans/update/<loan_id>/
    Typically used to mark a book as returned.
    Body: { "is_returned": true, "date_returned": "2025-02-01" }
    """
    if request.method != "PUT":
        return JsonResponse({"error": "Only PUT allowed"}, status=405)
    try:
        loan = LoanRecord.objects.get(id=loan_id)
    except LoanRecord.DoesNotExist:
        return JsonResponse({"error": "Loan record not found"}, status=404)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    loan.is_returned   = data.get("is_returned", loan.is_returned)
    loan.date_returned = data.get("date_returned", loan.date_returned)
    loan.save()
    return JsonResponse({"message": "Loan record updated successfully"})
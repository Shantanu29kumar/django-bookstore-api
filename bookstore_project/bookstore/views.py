from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Book
from django.forms.models import model_to_dict

@csrf_exempt
def create_book(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)

        book = Book.objects.create(
            book_name=data.get("book_name"),
            book_id=data.get("book_id"),
            lender_name=data.get("lender_name"),
            phone_number=data.get("phone_number"),
            date_given=data.get("date_given"),
            date_returned=data.get("date_returned"),
            is_returned=data.get("is_returned", True)
        )

        return JsonResponse({
            "message": "Book created successfully",
            "book_id": book.book_id
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_books(request):
    if request.method == "GET":
        books = Book.objects.all()
        books_list = [model_to_dict(book) for book in books]
        return JsonResponse(books_list,safe=False)
    
    return JsonResponse({"error":"Invalid method"},status = 400)

@require_http_methods(["GET"])
def get_book(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    data = {
        "book_id": book.book_id,
        "book_name": book.book_name,
        "lender_name": book.lender_name,
        "phone_number": book.phone_number,
        "is_returned": book.is_returned,
    }

    return JsonResponse(data)

@csrf_exempt
@require_http_methods(["PUT"])
def update_book(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    data = json.loads(request.body)

    book.book_name = data.get("book_name", book.book_name)
    book.lender_name = data.get("lender_name", book.lender_name)
    book.phone_number = data.get("phone_number", book.phone_number)
    book.is_returned = data.get("is_returned", book.is_returned)

    book.save()

    return JsonResponse({"message": "Book updated successfully"})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_book(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    book.delete()

    return JsonResponse({"message": "Book deleted successfully"})
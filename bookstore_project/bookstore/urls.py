from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_book),
    path("", views.get_books),
    path("<str:book_id>/", views.get_book),
    path("update/<str:book_id>/", views.update_book),
    path("delete/<str:book_id>/", views.delete_book),
]
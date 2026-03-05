from django.urls import path
from . import views

urlpatterns = [
    # ── Books ──────────────────────────────────────────
    path("",                        views.get_books),
    path("create/",                 views.create_book),
    path("update/<str:book_id>/",   views.update_book),
    path("delete/<str:book_id>/",   views.delete_book),

    # ── Authors ────────────────────────────────────────
    path("authors/",                    views.get_authors),
    path("authors/create/",             views.create_author),
    path("authors/<int:author_id>/",    views.get_author),

    # ── Borrowers ──────────────────────────────────────
    path("borrowers/",                  views.get_borrowers),
    path("borrowers/create/",           views.create_borrower),

    # ── Loan Records ───────────────────────────────────
    path("loans/",                      views.get_loans),
    path("loans/create/",               views.create_loan),
    path("loans/update/<int:loan_id>/", views.update_loan),

    # ── Keep this LAST since it matches anything ───────
    path("<str:book_id>/",              views.get_book),
]
# 📚 Bookstore API — Django REST Project

A Django-based REST API for managing a bookstore's books, authors, borrowers, and loan records. Built with plain Django (no DRF), using JSON views, CORS support, and a custom logging middleware.

---

## 🗂️ Project Structure

```
bookstore_project/
├── bookstore/
│   ├── models.py        # Author, Book, Borrower, LoanRecord
│   ├── views.py         # All API logic (JSON responses)
│   ├── urls.py          # App-level URL routing
│   ├── middleware.py    # Custom request/response logger
│   ├── admin.py
│   └── migrations/
├── bookstore_project/
│   ├── settings.py      # CORS, middleware, app config
│   └── urls.py          # Root URL config
├── manage.py
└── db.sqlite3
```

---

## 🗃️ Database Schema

```
┌─────────────────────────────┐
│           Author            │
├─────────────────────────────┤
│ id          (PK, auto)      │
│ name        CharField       │
│ email       EmailField      │
│ bio         TextField       │
└──────────────┬──────────────┘
               │ 1
               │
               │ Many
┌──────────────▼──────────────┐
│            Book             │
├─────────────────────────────┤
│ id          (PK, auto)      │
│ book_id     CharField (UK)  │◄── unique identifier (e.g. "HP001")
│ book_name   CharField       │
│ author      FK → Author     │
│ created_at  DateTimeField   │
└──────────────┬──────────────┘
               │ 1
               │
               │ Many
┌──────────────▼──────────────┐       ┌─────────────────────────────┐
│         LoanRecord          │       │          Borrower            │
├─────────────────────────────┤       ├─────────────────────────────┤
│ id            (PK, auto)    │       │ id           (PK, auto)     │
│ book          FK → Book     │       │ name         CharField      │
│ borrower      FK → Borrower │◄──────│ phone_number CharField      │
│ date_given    DateField     │  Many │ email        EmailField     │
│ date_returned DateField     │       └─────────────────────────────┘
│ is_returned   BooleanField  │
│ created_at    DateTimeField │
└─────────────────────────────┘
```

### Relationships at a glance

| Relationship | Type |
|---|---|
| Author → Book | One-to-Many (one author can have many books) |
| Book → LoanRecord | One-to-Many (one book can be loaned multiple times) |
| Borrower → LoanRecord | One-to-Many (one borrower can borrow many books) |

---

## ⚙️ Features

- **CRUD for Books** — create, list, get by ID, update, delete
- **Author management** — create authors, list all, view with their books
- **Borrower management** — create and list borrowers
- **Loan Record tracking** — issue a book to a borrower, mark it as returned
- **CORS enabled** — accepts requests from any origin (`CORS_ALLOW_ALL_ORIGINS = True`)
- **Custom middleware** — logs every request method, path, response status, and time taken
- **CSRF exempt** on all write endpoints (suitable for Postman / frontend calls)

---

## 🚀 Setup & Running

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install django django-cors-headers

# 3. Run migrations
python manage.py migrate

# 4. Start the server
python manage.py runserver
```

---

## 🔗 API Endpoints

Base URL: `http://127.0.0.1:8000/books`

### Authors

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/authors/` | List all authors |
| `POST` | `/authors/create/` | Create a new author |
| `GET` | `/authors/<id>/` | Get author + their books |

**Create Author — request body:**
```json
{
  "name": "J.K. Rowling",
  "email": "jk@example.com",
  "bio": "British author of Harry Potter"
}
```

---

### Books

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/` | List all books |
| `POST` | `/create/` | Create a new book |
| `GET` | `/<book_id>/` | Get a single book |
| `PUT` | `/update/<book_id>/` | Update a book |
| `DELETE` | `/delete/<book_id>/` | Delete a book |

**Create Book — request body:**
```json
{
  "book_name": "Harry Potter and the Philosopher's Stone",
  "book_id": "HP001",
  "author_id": 1
}
```

---

### Borrowers

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/borrowers/` | List all borrowers |
| `POST` | `/borrowers/create/` | Create a new borrower |

**Create Borrower — request body:**
```json
{
  "name": "Ravi Kumar",
  "phone_number": "9876543210",
  "email": "ravi@example.com"
}
```

---

### Loan Records

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/loans/` | List all loan records |
| `POST` | `/loans/create/` | Issue a book to a borrower |
| `PUT` | `/loans/update/<id>/` | Mark a book as returned |

**Create Loan — request body:**
```json
{
  "book_id": "HP001",
  "borrower_id": 1,
  "date_given": "2025-03-01",
  "is_returned": false
}
```

**Update Loan (return a book) — request body:**
```json
{
  "is_returned": true,
  "date_returned": "2025-03-15"
}
```

---

## 🔄 Recommended Order for Filling the DB

Since models have foreign key dependencies, always create in this order:

```
1. Author       →   POST /books/authors/create/
2. Book         →   POST /books/create/          (needs author_id)
3. Borrower     →   POST /books/borrowers/create/
4. Loan Record  →   POST /books/loans/create/    (needs book_id + borrower_id)
```

---

## 🛠️ Custom Middleware — APILogMiddleware

Located in `bookstore/middleware.py`. Automatically logs every request to the console:

```
Incoming Request: POST /books/create/
Response Status: 201
Time Taken: 0.0031s
```

---

## 🌐 CORS Configuration

Configured in `settings.py` to allow all origins — useful during development with a frontend or Postman:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

For production, replace with:
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourfrontend.com",
]
```
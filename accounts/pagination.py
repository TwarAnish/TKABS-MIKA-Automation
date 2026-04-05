# accounts/pagination.py
from rest_framework.pagination import CursorPagination

class CustomUserCursorPagination(CursorPagination):
    ordering = '-id' # Use the 'id' field for cursor-based pagination
    # You can also set other attributes like:
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
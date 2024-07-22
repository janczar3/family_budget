from rest_framework.pagination import PageNumberPagination


class BudgetPagination(PageNumberPagination):
    """Custom pagination for Budgets."""

    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 5

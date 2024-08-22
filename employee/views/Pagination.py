from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to set page size
    max_page_size = 100  # Max page size allowed
    

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            return self.invalid_page_error()

    def get_paginated_response(self, data):
        # Check if data is empty and if `self.page` exists
        if not data or not hasattr(self, 'page'):
            return Response({
                'results': [],
                'message': 'No data available.'
            })

        # Return the usual paginated response if data is not empty
        return Response({
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'results': data
        })

    def invalid_page_error(self):

        response_data = {
            "error": "Invalid page number.",
            "message": "The requested page does not exist."
        }
        raise NotFound(detail=response_data)
        
        print("invalid_page_error")
        # Return a custom response instead of raising an exception
        return Response({
            "error": "Invalid page number.",
            "message": "The requested page does not exist.",
            "total_items": self.page.paginator.count if hasattr(self, 'page') else 0,
            "total_pages": self.page.paginator.num_pages if hasattr(self, 'page') else 0
        })
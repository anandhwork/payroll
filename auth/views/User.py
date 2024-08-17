from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from auth.serializers.UserSerializer import UserSerializer

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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['username', 'email']
    ordering = ['-id']

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        # print(page.query)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):

        data = request.data

        if User.objects.filter(username=data["username"]).exists():
            return Response({
                    'status': 'success',
                    'data': "Username already exists"
                })

        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        serializer = self.get_serializer(user)

        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
        
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'User deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

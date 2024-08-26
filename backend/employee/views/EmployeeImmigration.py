from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from employee.views.Pagination import CustomPagination
from employee.models.EmployeeImmigration import EmployeeImmigration
from employee.serializers.EmployeeImmigration import EmployeeImmigrationSerializer

class EmployeeImmigrationViewSet(viewsets.ModelViewSet):
    queryset = EmployeeImmigration.objects.all()
    serializer_class = EmployeeImmigrationSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['visa_type']
    ordering = ['-employee_immigration_id']
    parser_classes = (MultiPartParser, FormParser)

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

        user_id = request.user.id

        data = request.data
        data["created_on"] = '2024-08-11 18:05:14'
        data["updated_on"] = '2024-08-11 18:05:14'
        data["created_by"] = user_id
        data["updated_by"] = user_id

        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({
                'status': 'failed',
                'data': serializer.errors
            })

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
        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response({
                'status': 'failed',
                'data': serializer.errors
            })
        
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Employee deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

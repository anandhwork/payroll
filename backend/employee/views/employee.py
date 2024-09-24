from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from employee.models.employee import Employee
from employee.serializers.employee import EmployeeSerializer
from employee.models.employeeEmergency import EmployeeEmergency
from employee.serializers.employeeEmergency import EmployeeEmergencySerializer
from employee.models.EmployeeImmigration import EmployeeImmigration
from employee.views.EmployeeImmigration import EmployeeImmigrationViewSet
from employee.helpers.AppHelper import AppHelper

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

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['first_name', 'last_name']
    ordering = ['-employee_id']

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
        data["created_on"] = AppHelper.datetime()
        data["updated_on"] = AppHelper.datetime()
        data["created_by"] = user_id
        data["updated_by"] = user_id

        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            employee_id = serializer.data["employee_id"]

            # User create

            emergency_contact = data.get('emergency_contact')
            if emergency_contact:
                for contact in emergency_contact:
                    contact["employee_id"] = employee_id
                    EmergencySerializer = EmployeeEmergencySerializer(data=contact, many=False)
                    if EmergencySerializer.is_valid():
                        EmergencySerializer.save()
                    else:
                        print(EmergencySerializer.errors)

            immigration_data = data.get('immigration')
            if immigration_data:
                immigration_data['employee_id'] = employee_id
                            
                # Using APIRequestFactory
                auth_header = request.headers.get('Authorization')
                token = auth_header.split()[1]
                factory = APIRequestFactory()
            
                t_request = factory.post('/api/immigration/', immigration_data, format='json')
                t_viewset = EmployeeImmigrationViewSet.as_view({'post': 'create'})
                t_request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
                immigration_response = t_viewset(t_request)

            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({
                'status': 'success',
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
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        employee_id = serializer.data["employee_id"]
        emergency_contact = request.data['emergency_contact']
        
        for contact in emergency_contact:
            contact["employee_id"] = employee_id
            EmergencySerializer = EmployeeEmergencySerializer(data=contact, many=False)
            if EmergencySerializer.is_valid():
                EmergencySerializer.save()
            else:
                print(EmergencySerializer.errors)

        immigration_data = request.data['immigration']
        if immigration_data:
            immigration_data['employee_id'] = employee_id
            
            immigration = EmployeeImmigration.objects.filter(employee_id=employee_id).first()
            
            # Using APIRequestFactory
            auth_header = request.headers.get('Authorization')
            token = auth_header.split()[1]
            factory = APIRequestFactory()
            
            if immigration:
                employee_immigration_id = immigration.employee_immigration_id
                t_request = factory.put('/api/immigration/{pk}/', immigration_data, format='json')
                t_viewset = EmployeeImmigrationViewSet.as_view({'put': 'update'})
                t_request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
                immigration_response = t_viewset(t_request, pk=employee_immigration_id)
            else:
                t_request = factory.post('/api/immigration/', immigration_data, format='json')
                t_viewset = EmployeeImmigrationViewSet.as_view({'post': 'create'})
                t_request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
                immigration_response = t_viewset(t_request)


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

    @action(methods=["GET"], detail=False)
    def listget(self, request):
        
        print("listget")
        return Response({'listget'})

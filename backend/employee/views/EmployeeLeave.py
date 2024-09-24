from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from employee.helpers.AppHelper import AppHelper

from employee.views.Pagination import CustomPagination
from employee.models.EmployeeLeaveType import EmployeeLeaveType
from employee.serializers.EmployeeLeaveType import EmployeeLeaveTypeSerializer
from employee.models.EmployeeLeaveRequest import EmployeeLeaveRequest
from employee.serializers.EmployeeLeaveRequest import EmployeeLeaveRequestSerializer
from employee.models.EmployeeLeaveRequestHistory import EmployeeLeaveRequestHistory
from employee.serializers.EmployeeLeaveRequestHistory import EmployeeLeaveRequestHistorySerializer

class EmployeeLeaveViewSet(viewsets.ModelViewSet):
    queryset = EmployeeLeaveRequest.objects.all()
    serializer_class = EmployeeLeaveRequestSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['start_date','end_date', 'note']
    ordering = ['-leave_request_id']

    @action(methods=["GET"], detail=False)
    def add(self, request):

        queryset = EmployeeLeaveType.objects.all()

        serializer = EmployeeLeaveTypeSerializer(queryset, many=True)

        response = {}
        response['leave_type'] = serializer.data
        return Response({
            'status': 'success',
            'data': response
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

            # Need to send mail to notify the user
            subject = 'Anandh has requested for leave'
            message = f'Hi anandh, Need to add leave details.'
            # AppHelper.send_notification_email(user.email, subject, message)

            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({
                'status': 'failed',
                'data': serializer.errors
            })
        
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

        user_id = request.user.id

        data = request.data
        data["updated_on"] = AppHelper.datetime()
        data["created_by"] = user_id
        data["updated_by"] = user_id
        

        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            # Update leave request status from user
            if "update_type" in data and data["updated_by"] == 2:
                pass

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
            'message': 'Leave Request deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

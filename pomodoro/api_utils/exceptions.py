
from rest_framework.exceptions import APIException
from rest_framework import status


class DeleteException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Failed to delete the model instance.'
    default_code = 'delete_failed'

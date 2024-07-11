from functools import wraps
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response


def handle_exception(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except Http404:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except ValidationError as e:
            response = {
                "status": "error",
                "errors": e.detail  
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error':str(e), 'status':status.HTTP_500_INTERNAL_SERVER_ERROR})
    return inner_func

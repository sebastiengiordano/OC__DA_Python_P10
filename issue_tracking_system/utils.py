from django.db import IntegrityError
from django.http import Http404
from rest_framework import status
from rest_framework.views import Response, exception_handler

from .views import ProjectView, IssueView


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    # to get the standard error response.
    response = exception_handler(exc, context)
    request = context['request']

    # if there is an IntegrityError and
    # it concerned the post methode to add contributor
    if (
            isinstance(exc, IntegrityError)
            and isinstance(context.get('view'), ProjectView)
            and 'POST' in dir(request)
            and hasattr(context.get('view'), 'action')
            and context['view'].action == 'manage_contributor'):
        user = request.user
        user_name = user.first_name + " " + user.last_name
        project_id = context['kwargs']['project_id']
        response = Response(
            {
                "non_field_errors": [
                    "The fields user, project must make a unique set. "
                    f"{user_name} is already a contributor "
                    f"of project n°{project_id}."
                    ]
            },
            status=status.HTTP_400_BAD_REQUEST)

    # Else if there is an IntegrityError and
    # it concerned the post methode to add an issue
    elif (
            isinstance(exc, IntegrityError)
            and isinstance(context.get('view'), IssueView)
            and 'POST' in dir(request)):
        user = request.user
        project_id = context['kwargs']['project_id']
        response = Response(
            {
                "non_field_errors": [
                    "The fields title must make a unique for the "
                    f"project n°{project_id}."
                    ]
            },
            status=status.HTTP_400_BAD_REQUEST)

    # Else if there is an Http404 response
    # send more explicit response
    elif isinstance(exc, Http404):
        response = Response(
            {
                "detail_not_found": [
                    f"{exc.args[0]}"
                    ]
            },
            status=status.HTTP_404_NOT_FOUND
        )

    return response

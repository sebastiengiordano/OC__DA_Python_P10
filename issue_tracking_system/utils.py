from django.db import IntegrityError
from rest_framework.views import Response, exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # if there is an IntegrityError and it concerned the post methode to add contributor
    if (
            isinstance(exc, IntegrityError)
            and 'POST' in dir(context['request'])
            and context['view'].action == 'manage_contributor'):
        user = context['request'].user
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
            status=status.HTTP_400_BAD_REQUEST
        )

    return response

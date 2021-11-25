from rest_framework import serializers

from issue_tracking_system.models import Projects


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = [
            'title',
            'description',
            'type',
            'author_user_id',
            'date_created',
            'date_updated'
            ]

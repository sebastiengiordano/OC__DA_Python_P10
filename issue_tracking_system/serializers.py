from django.db import models

from rest_framework import serializers

from issue_tracking_system.models import Projects, Contributors


class ProjectsSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Projects
        fields = [
            'id',
            'title',
            'description',
            'type',
            'author_user_id',
            'date_created',
            'date_updated'
            ]


class ContributorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = [
            'user_id',
            'project_id',
            'permission',
            'role',
            'date_created',
            'date_updated'
            ]

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from issue_tracking_system.models import Projects, Contributors,\
    CONTRIBUTORS_PERMISSIONS


class ProjectsSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    title = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Projects.objects.all())])
    description = serializers.TextField(required=True)
    type = serializers.CharField(required=True)
    author_user_id = 

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

    def create(self, validated_data):
        """
        Creates and saves a Projects and a Contributors with all permissions,
        since its the project's author.
        """
        project = Projects.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            type=validated_data['type'],
            author_user_id=self.user.id
        )
        Contributors.objects.create(
            user_id=self.user.id,
            project_id=project.id,
            permission=CONTRIBUTORS_PERMISSIONS['All'],
            role='author'
        )
        return project

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()

        password = validated_data.get('password', None)
        password_check = validated_data.get('password_check', None)

        if password and password_check and password == password_check:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)

        return instance


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

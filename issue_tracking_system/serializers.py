from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.validators import UniqueValidator

from issue_tracking_system.models import Projects, Contributors,\
    CONTRIBUTORS_PERMISSIONS


class ProjectsSerializer(serializers.ModelSerializer):
    '''Serializer of project.'''

    project_id = serializers.SerializerMethodField()
    # title = serializers.CharField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=Projects.objects.all())])
    # description = serializers.TextField(required=True)
    # type = serializers.CharField(required=True)
    author_user_id = serializers.SerializerMethodField()

    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = [
            'project_id',
            'title',
            'description',
            'type',
            'author_user_id',
            'contributors',
            'date_created',
            'date_updated'
            ]

    def create(self, validated_data):
        """Creates and saves a Projects and
        a Contributors with all permissions (since its the project's author).
        """

        # Get the current user
        user =  self.context['request'].user
        # Create the project
        project = Projects.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            type=validated_data['type'],
            author=user
            )
        # Add the author as contributor
        project_contributor = Contributors.objects.create(
            user=user,
            project=project,
            permission='All',
            role='author'
            )
        # If project and contributor are well created,
        # they could be save in DB.
        # project.save()
        # project_contributor.save()
        return project

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

    def get_project_id(self, instance):
        return instance.id

    def get_author_user_id(self, instance):
        return instance.author.id

    def get_contributors(self, instance):
        queryset = instance.project_contributor.all()
        serializer = ContributorsSerializer(queryset, many=True)
        return serializer.data


class ContributorsSerializer(serializers.ModelSerializer):
    '''Serializer of contributor.'''

    user_id = serializers.SerializerMethodField(read_only=True)
    project_id = serializers.SerializerMethodField(read_only=True)

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

    def get_user_id(self, instance):
        return instance.user.id

    def get_project_id(self, instance):
        return instance.project.id

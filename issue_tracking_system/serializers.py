from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.validators import UniqueValidator

from issue_tracking_system.models import Projects, Contributors,\
    CONTRIBUTORS_PERMISSIONS


class ProjectsSerializer(serializers.ModelSerializer):
    '''Serializer of project.'''

    project_id = serializers.ReadOnlyField()
    # title = serializers.CharField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=Projects.objects.all())])
    # description = serializers.TextField(required=True)
    # type = serializers.CharField(required=True)
    author_user_id = serializers.ReadOnlyField()

    class Meta:
        model = Projects
        fields = [
            'project_id',
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
        user =  self.context['request'].user
        project = Projects.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            type=validated_data['type'],
            author=user
            )
        project.save()
        # contributors = Contributors.objects.create(
        #     user_id=self.user.id,
        #     project_id=project.id,
        #     permission=CONTRIBUTORS_PERMISSIONS['All'],
        #     role='author'
        #     )
        # contributors.save()
        project_contributor = Contributors.objects.create(
            user=user,
            project=project,
            permission=CONTRIBUTORS_PERMISSIONS['All'],
            role='author'
            )
        project_contributor.save()
        return project

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

    def get_project_id(self, obj):
        return obj.project.id

    def get_author_user_id(self, obj):
        return obj.project.author.id


class ContributorsSerializer(serializers.ModelSerializer):
    '''Serializer of contributor.'''

    user_id = serializers.SerializerMethodField(read_only=True)
    project_id = serializers.SerializerMethodField(ReadOnlyField)

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

    def get_user_id(self, obj):
        return obj.user.id

    def get_project_id(self, obj):
        return obj.project.id

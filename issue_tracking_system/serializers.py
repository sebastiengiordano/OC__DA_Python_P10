from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from issue_tracking_system.models import Projects, Contributors


class ProjectsSerializerMethods(serializers.ModelSerializer):
    '''Methods used for project's serializers.'''

    def create(self, validated_data):
        """Creates and saves a Projects and
        a Contributors with all permissions (since its the project's author).
        """

        # Get the current user
        user = self.context['request'].user
        # Create the project
        project = Projects.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            type=validated_data['type'],
            author=user
            )
        # Add the author as contributor
        Contributors.objects.create(
            user=user,
            project=project,
            permission='All',
            role='author'
            )
        return project

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description',
            instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

    def get_project_id(self, instance):
        return instance.id

    def get_author_user_id(self, instance):
        return instance.author.id

    def get_author_user_email(self, instance):
        return instance.author.email

    def get_contributors(self, instance):
        queryset = instance.project_contributor.all()
        serializer = ContributorsSerializer(queryset, many=True)
        return serializer.data


class ProjectsSerializer(ProjectsSerializerMethods):
    '''Serializer of project.'''

    project_id = serializers.SerializerMethodField()
    author_user_id = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = [
            'project_id',
            'title',
            'description',
            'type',
            'author_user_id'
            ]


class ProjectsDetailSerializer(ProjectsSerializerMethods):
    '''Detail serializer of project.'''

    project_id = serializers.SerializerMethodField()
    author_user_id = serializers.SerializerMethodField()
    author_user_email = serializers.SerializerMethodField()

    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = [
            'project_id',
            'title',
            'description',
            'type',
            'author_user_id',
            'author_user_email',
            'contributors',
            'date_created',
            'date_updated'
            ]


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
        validators = [
            UniqueTogetherValidator(
                queryset=Contributors.objects.all(),
                fields=['user_id', 'project_id']
            )
        ]

    def get_user_id(self, instance):
        return instance.user.id

    def get_project_id(self, instance):
        return instance.project.id


class ManageContributorSerializer(serializers.Serializer):
    '''Serializer to check request which add a new contributor to a project.'''

    email = serializers.EmailField(write_only=True)

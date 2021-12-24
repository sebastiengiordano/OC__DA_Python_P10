from rest_framework import serializers

from .models import Projects, Contributors, Issues, Comments


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
    user_email = serializers.SerializerMethodField(read_only=True)
    project_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contributors
        fields = [
            'user_id',
            'user_email',
            'project_id',
            'permission',
            'role'
            ]

    def get_user_id(self, instance):
        return instance.user.id

    def get_user_email(self, instance):
        return instance.user.email

    def get_project_id(self, instance):
        return instance.project.id


class ManageContributorSerializer(serializers.Serializer):
    '''Serializer to check request which add a new contributor to a project.'''

    email = serializers.EmailField(write_only=True)


class SerializerMethods(serializers.ModelSerializer):
    '''Methods used for issue's serializers and comment's serializers.'''

    def get_issue_id(self, instance):
        return instance.id

    def get_project_id(self, instance):
        return instance.project.id

    def get_comment_id(self, instance):
        return instance.id

    def get_author_id(self, instance):
        return instance.author.id

    def get_assignee_id(self, instance):
        return instance.assignee.id

    def get_author_email(self, instance):
        return instance.author.email

    def get_assignee_email(self, instance):
        return instance.assignee.email


class IssuesSerializer(SerializerMethods):
    '''Serializer of issue.'''

    issue_id = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.SerializerMethodField(read_only=True)
    assignee_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Issues
        fields = [
            'issue_id',
            'title',
            'project_id',
            'author_id',
            'assignee_id'
            ]


class IssuesDetailSerializer(IssuesSerializer):
    '''Serializer of issue for detail view.'''

    author_email = serializers.SerializerMethodField(read_only=True)
    assignee_email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Issues
        fields = [
            'issue_id',
            'title',
            'description',
            'tag',
            'priority',
            'project_id',
            'status',
            'author_id',
            'author_email',
            'assignee_id',
            'assignee_email',
            'date_created',
            'date_updated'
            ]


class IssuesUpdateSerializer(serializers.ModelSerializer):
    '''Serializer of issue for update purpose.'''

    class Meta:
        model = Issues
        fields = [
            'title',
            'description',
            'tag',
            'priority',
            'project',
            'status',
            'author',
            'assignee'
            ]

    def get_unique_together_validators(self):
        return []


class CommentsSerializer(SerializerMethods):
    '''Serializer of comment.'''

    comment_id = serializers.SerializerMethodField()
    issue_id = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comments
        fields = [
            'comment_id',
            'description',
            'author_id',
            'author_email',
            'issue_id',
            ]


class CommentsUpdateSerializer(SerializerMethods):
    '''Serializer of comment for update purpose.'''

    class Meta:
        model = Comments
        fields = [
            'description'
            ]

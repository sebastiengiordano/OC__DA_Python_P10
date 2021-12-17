from django.db import models
from django.conf import settings


PROJECT_TYPE = (
    ('Back-end', 'Back-end'),
    ('Front-end', 'Front-end'),
    ('iOS', 'iOS',),
    ('Android', 'Android')
    )

CONTRIBUTORS_PERMISSIONS = (
    ('All', 'All'),
    ('Read_Only', 'Read_Only')
)

TAG_ISSUE = (
    ('Bug', 'Bug'),
    ('Improvement', 'Improvement'),
    ('Task', 'Task'),
)

PRIORITY_ISSUE = (
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
)

STATUS_ISSUE = (
    ('To_Do', 'To_Do'),
    ('In_Progress', 'In_Progress'),
    ('Completed', 'Completed'),
)


class Projects(models.Model):
    '''This class aims to defined projects.'''

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    title = models.CharField(
                            verbose_name='title',
                            max_length=255,
                            unique=True,
                            blank=False)
    description = models.TextField(blank=False)
    type = models.CharField(
                            max_length=10,
                            choices=PROJECT_TYPE,
                            blank=False)
    author = models.ForeignKey(
                            'accounts.CustomUser',
                            on_delete=models.CASCADE,
                            related_name='author')

    REQUIRED_FIELDS = ['title', 'description', 'type', 'author']

    def __str__(self):
        return self.title


class Contributors(models.Model):
    '''This class aims to defined contributors.'''

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='user_contributor',
                                default=0)
    project = models.ForeignKey(
                                'issue_tracking_system.Projects',
                                on_delete=models.CASCADE,
                                related_name='project_contributor',
                                default=0)
    permission = models.CharField(
                                max_length=10,
                                choices=CONTRIBUTORS_PERMISSIONS)
    role = models.CharField(
                                verbose_name='role',
                                max_length=255)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return (
            "Contributors"
            f"\n\tid: {self.user.id}"
            f"\n\tproject id: {self.project.id}"
            f"\n\tproject title: {self.project.title}")


class Issues(models.Model):
    '''This class aims to defined issues.'''

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    title = models.CharField(
                            verbose_name='title',
                            max_length=255,
                            blank=False)
    description = models.TextField(blank=False)
    tag = models.CharField(
                            max_length=11,
                            choices=TAG_ISSUE,
                            blank=False)
    priority = models.CharField(
                            max_length=6,
                            choices=PRIORITY_ISSUE,
                            blank=False)
    status = models.CharField(
                            max_length=11,
                            choices=STATUS_ISSUE,
                            blank=False)
    project = models.ForeignKey(
                                'issue_tracking_system.Projects',
                                on_delete=models.CASCADE,
                                related_name='project_issue',
                                default=0)
    author = models.ForeignKey(
                            'accounts.CustomUser',
                            on_delete=models.CASCADE,
                            related_name='author_issue')
    assignee = models.ForeignKey(
                            'accounts.CustomUser',
                            on_delete=models.CASCADE,
                            related_name='assignee')

    REQUIRED_FIELDS = ['title', 'description', 'tag', 'priority', 'status']

    class Meta:
        unique_together = ('title', 'project')

    def __str__(self):
        return (
            "Issue"
            f"\n\tid: {self.id}"
            f"\n\tid: {self.title}"
            f"\n\tproject id: {self.project.id}"
            f"\n\tproject title: {self.project.title}")

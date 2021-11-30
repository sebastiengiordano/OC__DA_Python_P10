from django.db import models
from django.conf import settings


PROJECT_TYPE = (
    ('Back-end', 'Back-end'),
    ('Front-end', 'Front-end'),
    ('iOS', 'iOS',),
    ('Android', 'Android')
    )

CONTRIBUTORS_PERMISSIONS = [
    ('All', 'All'),
    ('Read_Only', 'Read_Only')
]


class Projects(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    title = models.CharField(
                            verbose_name='title',
                            max_length=255)
    description = models.TextField(blank=False)
    type = models.CharField(
                            max_length=10,
                            choices=PROJECT_TYPE)
    author_user_id = models.ForeignKey(
                                        'accounts.CustomUser',
                                        on_delete=models.CASCADE,
                                        related_name='author_user_id')

    REQUIRED_FIELDS = ['title', 'description', 'type', 'author_user_id']

    def __str__(self):
        return self.title


class Contributors(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    user_id = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='user_id',
                                default=0)
    project_id = models.ForeignKey(
                                    'issue_tracking_system.Projects',
                                    on_delete=models.CASCADE,
                                    verbose_name='project_id',
                                    default=0)
    permission = models.CharField(
                                    max_length=10,
                                    choices=CONTRIBUTORS_PERMISSIONS)
    role = models.CharField(
                            verbose_name='role',
                            max_length=255)

    REQUIRED_FIELDS = ['user_id', 'project_id']

    def __str__(self):
        return (
            "Contributors"
            "\n\tid: {self.user_id}"
            "\n\tproject id: {self.project_id}")

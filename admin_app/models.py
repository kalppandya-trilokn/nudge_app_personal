from django.db import models


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = True
        db_table = 'alembic_version'


class Users(models.Model):
    STATUS_ACTIVE = 1
    STATUS_SUSPENDED = 2
    STATUS_BLOCKED = 3

    STATUS_CHOICES = (
        (STATUS_ACTIVE, "Active"),
        (STATUS_SUSPENDED, "Suspended"),
        (STATUS_BLOCKED, "Blocked"),
    )

    phone_number = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    location = models.CharField(max_length=100)
    interests = models.TextField()
    personal_facts = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    suspended_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class ChatSessions(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, null=True, blank=True)
    message_count = models.IntegerField()
    last_activity_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'chat_sessions'

    def __str__(self):
        return f"Session {self.id} - {self.user.name if self.user else 'No User'}"


class Prompts(models.Model):
    text = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(blank=True, null=True)
    session_order = models.IntegerField()
    session = models.ForeignKey(ChatSessions, models.DO_NOTHING, default=1)
    moderation_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'prompts'
        verbose_name = "Prompt"
        verbose_name_plural = "Prompts"

    def __str__(self):
        return f"Prompt {self.id} - {self.text[:30]}..."

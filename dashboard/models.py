from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Device(models.Model):
    name = models.CharField(blank=True, unique=True, max_length=512)
    description = models.CharField(blank=True, max_length=512)
    notes = models.TextField(blank=True)
    markdown_enabled = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    ip_address = models.CharField(blank=True, max_length=64)
    is_live = models.BooleanField(null=True)
    is_public = models.BooleanField(default=False)
    public_key = models.CharField(blank=True, max_length=32)
    private_key = models.CharField(blank=True, max_length=64)
    hostname = models.CharField(blank=True, max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def markdown_enabled_string(self):
        return "t" if self.markdown_enabled else "f"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(blank=True)

    def get_picture_path(self, file_name):
        return f"profile_pictures/{self.user.username}/{file_name}"

    picture = models.ImageField(upload_to=get_picture_path, null=True)


class SocialConnection(models.Model):
    connectees = models.ManyToManyField(User)

    CONNECTION_OPTIONS = (
        ("FR", "Friend"),
        # More may be added in the future.
    )
    conn_type = models.CharField(max_length=2, default="FR", choices=CONNECTION_OPTIONS)

    created_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Project(models.Model):
    """data entry model for a project that an user can do, can either be a gif or still image project"""
    name = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    is_gif = models.BooleanField(null=False, default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    upload_version = models.ImageField(upload_to="images/")

    def __repr__(self) -> str:
        """returns the project name and the owner id that it belongs to"""
        cls = self.__class__.__name__
        return f"{cls} name={self.name!r} owner_id={self.user_id!r}"

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={ 'pk': self.pk })


class Image(models.Model):
    """data entry model for an image that can be inside a project"""
    project_id = models.ForeignKey(Project, null=False, on_delete=models.CASCADE)
    image_data = models.ImageField(upload_to="images/")
    date_created = models.DateTimeField(auto_now_add=True)
    animation_position = models.PositiveIntegerField(null=False, default=0)

    class Meta:
        ordering = ["animation_position"]

    def __repr__(self) -> str:
        """returns the image name and the project id that it belongs to"""
        cls = self.__class__.__name__
        return f"{cls} image_dir={self.image_data!r} project_id={self.project_id!r}"


class Comment(models.Model):
    """data entry model for a comment on a project or another comment"""
    content = models.TextField()
    post_id = models.ForeignKey(Project, null=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        """returns the user id of the author and the date created"""
        cls = self.__class__.__name__
        return f"{cls} user_id={self.user_id!r} date_created={self.date_created!r}"

from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.db import models


# Create your models here.
def get_profile_image_filepath(self, filename):
    """
    When User set his profile image, the uploaded imaged will be saved in
    a folder named as User primary key and within will be the uploaded image.
    """
    return f"{self.pk}/{filename}"


class User(models.Model):
    """
    User model defining a USER by it"s attributes and methods.
    """

    profile_image = models.ImageField(
        max_length=255, blank=True,
        upload_to=get_profile_image_filepath,
    )


"""
    A class to accomodate the following output:
    {
        'file_name': 
            [
                [
                    'filename1', 
                    'float value',
                    [str, str, ...] 
                ], 
                [
                    'file name', 
                    'float value',
                    [str, str, ...] 
                ], 
            ], ...   
    }, ...

 
"""

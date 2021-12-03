"""Circles  model."""

# Django
from django.db import models

# Utils
from cride.utils.models import CRideModel


class Circle(CRideModel):
    """Circle model.

      Circle is a private group. Yo Joain a circle yo need a unqiue invitation
    """

    name = models.CharField('Circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)
    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)
    members = models.ManyToManyField(
        'users.User',
        through='circles.Membership',
        through_fields=('circle', 'user')
    )

    # Stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField('verify circle', default=False,
                                   help_text='Verified circles are also kwnown as official')
    is_public = models.BooleanField(
        default=True, help_text='Public circles are listed in the main page so everyone known about their existence')
    is_limited = models.BooleanField(
        default=False, help_text='Limited circles can grow up to a fixed number of members.')
    members_limit = models.PositiveIntegerField(
        default=0, help_text='If circle is limited, this will be the maximum number of members in the circle')

    def __str__(self) -> str:
        """Return circle name"""
        return self.name

    class Meta(CRideModel.Meta):
        """Meta option"""
        ordering = ['-rides_taken', '-rides_offered']

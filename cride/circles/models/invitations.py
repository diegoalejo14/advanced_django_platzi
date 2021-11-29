# Django
from django.db import models


#Manager

from cride.circles.managers.invitations import InvitationManager

# Utilities
from cride.utils.models import CRideModel


class Invitation(CRideModel):
    """Circle Invitation

    """
    code = models.CharField(max_length=50, unique=True)
    issued_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='Circle member that invited you to join a circle',
        related_name='issued_by')
    used_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        help_text='User to join with this invitation',
        related_name='used_by')
    circle = models.ForeignKey(
        'circles.Circle',
        null=True,
        on_delete=models.CASCADE,
    )
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)



    #Manager
    objects=InvitationManager()

    def __str__(self) -> str:
        return '#{}:{}'.format(self.circle.slug_name,self.code)
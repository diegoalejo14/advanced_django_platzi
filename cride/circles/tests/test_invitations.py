"""Invitations test."""

# Django
from django.test import TestCase


# Django REst Framework
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


# Model
from cride.circles.models import Invitation, Circle, Membership
from cride.users.models import User, Profile


class InvitationsManagerTestCase(TestCase):
    """Invitations Manager test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Nombre1',
            last_name='Apellido1',
            email='Nombre1@jaja.com',
            username='nombre1',
            password='password1'
        )
        self.circle = Circle.objects.create(
            name='Javeriana',
            slug_name='Javeriana',
            about='Grupo oficial de la Facultad de Ciencias de la UNAM',
            verified=True
        )

    def test_code_generation(self):
        """Random codes should be generated automatically."""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        """If a code is given, there's no need to create a new one."""
        code = 'holamundo'
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicate(self):
        """If given code is not unique, a new one must be generated."""
        code = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
        ).code
        invitation2 = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertNotEqual(code, invitation2.code)


class MemberInvitationsAPITestCase(APITestCase):
    """Member invitation API test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Nombre1',
            last_name='Apellido1',
            email='Nombre1@jaja.com',
            username='nombre1',
            password='password1'
        )
        self.profile = Profile.objects.create(user=self.user)
        self.circle = Circle.objects.create(
            name='Javeriana',
            slug_name='Javeriana',
            about='Grupo oficial de la Facultad de Ciencias de la UNAM',
            verified=True
        )
        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitation=10
        )
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))

    def test_response_success(self):
        """Verify request suceed."""
        url = '/circles/{}/members/{}/invitations/'.format(
            self.circle.slug_name,
            self.user.username
        )
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Verify invitation are generated if none exist previously"""
        url = '/circles/{}/members/{}/invitations/'.format(
              self.circle.slug_name,
              self.user.username
        )
        #Invitations in DB must be 0
        self.assertEqual(Invitation.objects.count(),0)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        #Verify new invitations ware created
        invitations=Invitation.objects.filter(issued_by=self.user)
        self.assertEqual(invitations.count(),10)
        for invitation in invitations:
          self.assertIn(invitation.code,request.data['invitations'])


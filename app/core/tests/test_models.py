"""Tests for Models."""

from unittest import TestCase
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from core.models import User


class ModelTests(TestCase):
    """Test models."""

    def setUp(self):
        self.patcher = patch.object(
            User,
            User.save.__name__,
            return_value=None,
        )
        self.mock_save = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_create_user_with_email_successful(self):
        """Test create user with email successful"""
        email = "test@example.com"
        password = "testpass123"

        user: AbstractUser = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
        ]

        for email, expected in sample_emails:
            user: AbstractUser = get_user_model().objects.create_user(
                email=email,
            )

            self.assertEqual(user.email, expected)

    def test_create_user_with_empty_email_then_raise_value_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="password")

    def test_create_super_user(self):
        user: User = get_user_model().objects.create_superuser(
            "test@example.com",
            "password123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

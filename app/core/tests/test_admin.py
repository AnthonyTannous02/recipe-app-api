"""
Tests for Django admin modifications.
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from core.models import User


class AdminSiteTests(TestCase):
    """Tests for admin site."""

    def setUp(self):
        """Create User and Client."""
        user_manager = get_user_model().objects
        self.client = Client()
        self.admin_user: User = user_manager.create_superuser(
            email="admin@example.com",
            password="testpass123",
        )
        self.client.force_login(self.admin_user)
        self.user: User = user_manager.create_user(
            email="user@example.com",
            password="testpass123",
            name="Test User",
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Tests that the edit page is returned successfully."""
        url = reverse("admin:core_user_change", args=(self.user.id,))
        res = self.client.get(url)

        self.assertEqual(200, res.status_code)

    def test_create_user_page(self):
        """Test that changes users"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(200, res.status_code)

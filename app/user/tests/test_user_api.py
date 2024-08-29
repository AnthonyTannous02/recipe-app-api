"""
Tests for the User Api.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from user import (
    APP_NAME,
    CREATE_COMMAND,
    ME_COMMAND,
    TOKEN_COMMAND,
)


CREATE_USER_URL = reverse(APP_NAME + ":" + CREATE_COMMAND)
TOKEN_URL = reverse(APP_NAME + ":" + TOKEN_COMMAND)
ME_URL = reverse(APP_NAME + ":" + ME_COMMAND)


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests for public features of the user API."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user(self):
        payload = {
            "email": "test@example.com",
            "password": "test123",
            "name": "Test User",
        }

        res = self.client.post(CREATE_USER_URL, data=payload)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertEqual(payload["name"], user.name)
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        payload = {
            "email": "test@example.com",
            "password": "test123",
            "name": "Test User",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test User",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model()
            .objects.filter(
                email=payload["email"],
            )
            .exists()
        )
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "test-user-password",
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(status.HTTP_200_OK, res.status_code)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "test-user-password",
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": "badpass",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_create_token_blank_password(self):
        payload = {
            "email": "test@example.com",
            "password": "",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, res.status_code)


class PrivateUserApiTests(TestCase):
    """Test api requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email="user@example.com",
            password="testpass123",
            name="Test Name",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(
            {"email": self.user.email, "name": self.user.name},
            res.data,
        )

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, res.status_code)

    def test_update_user_profile(self):
        """Test updating data for the authenticated user."""
        payload = {
            "name": "Updated User",
            "password": "pass123Now",
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(payload["name"], self.user.name)
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(status.HTTP_200_OK, res.status_code)

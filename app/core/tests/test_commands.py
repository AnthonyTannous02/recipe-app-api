"""
Test custom Django management commands.
"""

import time
from unittest.mock import MagicMock, patch
from psycopg2 import OperationalError as PsyOperationalError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from core.management.commands.db_wait_service import Command


@patch.object(Command, Command.check.__name__)
class CommandTests(SimpleTestCase):
    """Test Commands."""

    def test_db_wait_service_ready(self, patched_check: MagicMock):
        """Test waiting for database if database ready."""

        patched_check.return_value = True

        call_command(Command())

        patched_check.assert_called_once_with(databases=["default"])

    @patch.object(time, time.sleep.__name__)
    def test_db_wait_service_delay(
        self, patched_sleep: MagicMock, patched_check: MagicMock
    ):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = (
            [PsyOperationalError] * 2 + [OperationalError] * 3 + [True]
        )
        # First error, database service not started -> PsyOpError
        # Second Error, Testing database was not set up yet -> OpError

        call_command(Command())

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])

# pylint: disable=R0903
# pylint: disable=W0104
# skipcq
"""
Pytest test file
"""


class TestClass:
    """Test class for gui.py"""

    def test_temp(self):  # skipcq: PYL-R0201
        """Temporary"""
        assert 1 + 1 == 2

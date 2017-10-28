from timereporter.__main__ import main
from unittest.mock import patch


class TestMain:
    @patch('timereporter.__main__.print', create=True)
    def test_no_arguments(self, print_):
        main()

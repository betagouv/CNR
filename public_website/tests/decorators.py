from unittest.mock import patch


def patch_send_in_blue(function_to_test):
    @patch("public_website.email_provider.send_payload_to_send_in_blue")
    def patched_function_to_test(self, mock_send_payload_to_send_in_blue):
        function_to_test(self)

    return patched_function_to_test

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def check_captcha_token(form_data):
    if settings.MOCK_EXTERNAL_API == "True":
        return True
    try:
        token = form_data["mtcaptcha-verifiedtoken"]
    except KeyError:
        return False
    private_key = settings.MTCAPTCHA_PRIVATE_KEY
    if not private_key:
        logger.exception("MTCAPTCHA_PRIVATE_KEY has not been set.")
        return False
    mtcaptcha_url = (
        "https://service.mtcaptcha.com/mtcv1/api/checktoken?privatekey="
        + private_key
        + "&token="
        + token
    )
    try:
        response = requests.get(mtcaptcha_url)
        if response.status_code == 200:
            try:
                success = response.json()["success"]
                if success:
                    return True
                else:
                    logger.exception("Token failed : %s", response.json()["fail_codes"])
                    return False
            except KeyError:
                return False
        else:
            logger.exception(
                "Bad status code when calling Mtcaptcha API-> check-token: %s", response
            )
            return False
    except Exception as e:
        logger.exception("Exception when calling Mtcaptcha API-> check-token: %s", e)
        return False

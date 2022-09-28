import logging

import sib_api_v3_sdk
from django.conf import settings
from django_rq import job
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


@job
def send_payload_to_send_in_blue_task(email: str, payload: dict) -> bool:
    if settings.MOCK_EXTERNAL_API == "True":
        return True
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.SEND_IN_BLUE_API_KEY
    try:
        api_instance = sib_api_v3_sdk.ContactsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        contact = sib_api_v3_sdk.CreateContact(
            email=email,
            update_enabled=True,
            attributes=payload,
            list_ids=[settings.SEND_IN_BLUE_LIST],
        )
        api_instance.create_contact(contact)
        return True
    except sib_api_v3_sdk.rest.ApiException as e:
        logger.exception("Exception when calling ContactsApi->create_contact: %s", e)
        raise

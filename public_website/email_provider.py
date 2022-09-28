import logging

import sib_api_v3_sdk
from django.conf import settings
from dotenv import load_dotenv

from public_website.models import Participant, Theme

load_dotenv()
logger = logging.getLogger(__name__)


def send_payload_to_send_in_blue(email: str, payload: dict) -> bool:
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


def create_payload_for_email_provider(participant: Participant):
    participant_type_mapping = {"PARTICULIER": 1, "ELU": 2, "ASSOCIATION": 3}
    try:
        participant_type = participant_type_mapping[participant.participant_type]
    except KeyError:
        logger.error(
            "%s does not exist in the participant_type_mapping dict", participant_type
        )
        raise
    subscription_list = participant.get_subscription_list()
    return {
        "PRENOM": participant.first_name,
        "PARTICIPANT_TYPE": participant_type,
        "CODE_POSTAL": participant.postal_code,
        "THEME_SANTE": Theme.SANTE in subscription_list,
        "THEME_EDUCATION": Theme.EDUCATION in subscription_list,
        "THEME_CLIMAT": Theme.CLIMAT in subscription_list,
        "THEME_VIEILLISSEMENT": Theme.VIEILLISSEMENT in subscription_list,
        "THEME_SOUVERAINETE": Theme.SOUVERAINETE in subscription_list,
        "THEME_TRAVAIL": Theme.TRAVAIL in subscription_list,
        "THEME_LOGEMENT": Theme.LOGEMENT in subscription_list,
        "THEME_JEUNESSE": Theme.JEUNESSE in subscription_list,
        "THEME_NUMERIQUE": Theme.NUMERIQUE in subscription_list,
    }


def send_participant_profile_to_email_provider(participant: Participant):
    try:
        if participant.has_profile:
            payload = create_payload_for_email_provider(participant)
        else:
            payload = {}
        send_payload_to_send_in_blue(participant.email, payload=payload)
    except Exception:
        return False
    return True

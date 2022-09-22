import logging

# import sib_api_v3_sdk
from dotenv import load_dotenv

from public_website.models import Participant, Theme

# import os


# from sib_api_v3_sdk.rest import ApiException


load_dotenv()
logger = logging.getLogger(__name__)


def send_payload_to_send_in_blue(email: str, attributes: dict) -> bool:
    return True
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = os.getenv("SEND_IN_BLUE")
    try:
        api_instance = sib_api_v3_sdk.ContactsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        contact = sib_api_v3_sdk.CreateContact(
            email=email, update_enabled=True, attributes=attributes, list_ids=[1]
        )
        api_instance.create_contact(contact)
        return True
    except ApiException as e:
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
        "THEME_SANTE": Theme.SANTE in subscription_list,
        "THEME_EDUCATION": Theme.EDUCATION in subscription_list,
        "PARTICIPANT_TYPE": participant_type,
        "CODE_POSTAL": participant.postal_code,
    }


def send_participant_profile_to_email_provider(participant: Participant):
    try:
        if participant.has_profile:            
            payload = create_payload_for_email_provider(participant)
        else: 
            payload = {}
        send_payload_to_send_in_blue(
            participant.email,
            payload=payload
        )
    except Exception:
        return False

    return True

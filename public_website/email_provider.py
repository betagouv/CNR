import logging

from dotenv import load_dotenv

from public_website.models import Participant, Theme

from .tasks import send_payload_to_send_in_blue_task

load_dotenv()
logger = logging.getLogger(__name__)


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
    print("send_participant_profile_to_email_provider")
    try:
        if participant.has_profile:
            payload = create_payload_for_email_provider(participant)
        else:
            payload = {}
        send_payload_to_send_in_blue_task.delay(participant.email, payload=payload)
    except Exception:
        return False
    return True

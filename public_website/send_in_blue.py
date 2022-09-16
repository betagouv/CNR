import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

load_dotenv()


def send_contact_to_send_in_blue(email, first_name, theme_sante, theme_education, participant_type_number, code_postal):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("SEND_IN_BLUE")

    api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
    create_contact = sib_api_v3_sdk.CreateContact(
        email=email,
        update_enabled=True,
        attributes={
            'PRENOM': first_name,
            'THEME_SANTE': theme_sante,
            "THEME_EDUCATION": theme_education,
            "PARTICIPANT_TYPE": participant_type_number,
            "CODE_POSTAL": code_postal
        },
        list_ids=[1])
    try:
        api_response = api_instance.create_contact(create_contact)
        print(api_response)
    except ApiException as e:
        print("Exception when calling ContactsApi->create_contact: %s\n" % e)

send_contact_to_send_in_blue("example4@example.com", 'JON', True, True, "1",
                                 "75009")

    #   "name": "THEMES",
    #   "category": "category",
    #   "enumeration": [
    #     {
    #       "value": 1,
    #       "label": "santé"
    #     },
    #     {
    #       "value": 2,
    #       "label": "éducation"
    #     }
    #   ]
    # },
    # {
    #   "name": "PARTICIPANT_TYPE",
    #   "category": "category",
    #   "enumeration": [
    #     {
    #       "value": 1,
    #       "label": "citoyen"
    #     },
    #     {
    #       "value": 2,
    #       "label": "élu"
    #     },
    #     {
    #       "value": 3,
    #       "label": "representant_association"
    #     }
    #   ]
    # },
    # {
    #   "name": "CODE_POSTAL",
    #   "category": "normal",
    #   "type": "text"
    # }

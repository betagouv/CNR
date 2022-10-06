from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm

from public_website.captcha import check_captcha_token

from . import models


class RegisterForm(Form):

    email = forms.EmailField(
        label="Inscrivez-vous à notre infolettre et choisissez votre niveau de participation",
    )

    gives_gdpr_consent = forms.BooleanField(
        required=True,
    )

    def is_captcha_valid(self):
        return check_captcha_token(self.data)


class ProfileForm(ModelForm):

    email = forms.EmailField(
        label="Adresse électronique",
    )

    participant_type = forms.ChoiceField(
        choices=models.ParticipantType.choices,
        widget=forms.RadioSelect,
        label="Je suis",
    )

    sante_participant_type = forms.ChoiceField(
        choices=models.SanteParticipantType.choices,
        widget=forms.RadioSelect,
        label="Je participe en tant que :",
        required=False,
    )

    education_participant_type = forms.ChoiceField(
        choices=models.EducationParticipantType.choices,
        widget=forms.RadioSelect,
        label="Je participe en tant que :",
        required=False,
    )

    available_themes = []
    unavailable_themes = [models.Theme.SANTE, models.Theme.EDUCATION]
    for choice in models.Theme.choices:
        if choice[0] not in unavailable_themes:
            available_themes.append(choice)

    preferred_themes = forms.MultipleChoiceField(
        choices=available_themes,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    gives_gdpr_consent = forms.BooleanField()

    pick_local_theme_sante = forms.BooleanField(
        label="Pour améliorer notre santé", required=False
    )

    pick_local_theme_education = forms.BooleanField(
        label="Pour améliorer notre école", required=False
    )

    def is_captcha_valid(self):
        return check_captcha_token(self.data)

    def clean_postal_code(self):
        postal_code = self.cleaned_data["postal_code"]
        for character in postal_code:
            if not character.isdigit():
                raise ValidationError(
                    "The postal code must only contain numbers."
                    " If you live abroad, please input 99"
                )
        if len(postal_code) != 5 and postal_code != "99":
            raise ValidationError(
                "This postal Code is too short. If you live abroad, please input 99"
            )
        return postal_code

    class Meta:
        model = models.Participant
        fields = [
            "first_name",
            "postal_code",
            "participant_type",
            "sante_city",
            "sante_participant_type",
            "education_city",
            "education_participant_type",
        ]

    def save(self, commit=True, *args, **kwargs):
        instance = super(ProfileForm, self).save(commit=False)
        instance.email = self.cleaned_data["email"]
        instance.save()
        preferred_themes = self.cleaned_data["preferred_themes"]
        for theme in preferred_themes:
            subscription = models.Subscription(participant_id=instance.id, theme=theme)
            subscription.save()
        if self.cleaned_data["pick_local_theme_sante"]:
            subscription = models.Subscription(
                participant_id=instance.id, theme="SANTE"
            )
            subscription.save()
        else:
            if self.cleaned_data["sante_city"]:
                instance.sante_city = None
            if self.cleaned_data["sante_participant_type"]:
                instance.sante_participant_type = None

        if self.cleaned_data["pick_local_theme_education"]:
            subscription = models.Subscription(
                participant_id=instance.id, theme="EDUCATION"
            )
            subscription.save()
        else:
            if self.cleaned_data["education_city"]:
                instance.education_city = None
            if self.cleaned_data["education_participant_type"]:
                instance.education_participant_type = None

        return instance

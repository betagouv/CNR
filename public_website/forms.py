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
        label="J'ai lu et j'accepte les CGU et la politique de protection des données",
        required=True,
    )

    def is_captcha_valid(self):
        return check_captcha_token(self.data["csrfmiddlewaretoken"])


class ProfileForm(ModelForm):

    email = forms.EmailField(
        label="Adresse électronique",
    )

    participant_type = forms.ChoiceField(
        choices=models.ParticipantType.choices,
        widget=forms.RadioSelect,
        label="Je suis :",
    )

    preferred_themes = forms.MultipleChoiceField(
        choices=models.Theme.choices,
        widget=forms.CheckboxSelectMultiple,
        label="Les thématiques sur lesquelles je veux m'investir :",
    )

    gives_gdpr_consent = forms.BooleanField(
        label="J'ai lu et j'accepte les CGU et la politique de protection des données",
    )

    def is_captcha_valid(self):
        return check_captcha_token(self.data["csrfmiddlewaretoken"])

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
        fields = ["first_name", "postal_code", "participant_type"]

    def save(self, commit=True, *args, **kwargs):
        instance = super(ProfileForm, self).save(commit=commit)
        instance.email = self.cleaned_data["email"]
        preferred_themes = self.cleaned_data["preferred_themes"]
        for theme in preferred_themes:
            subscription = models.Subscription(participant_id=instance.id, theme=theme)
            subscription.save()
        return instance

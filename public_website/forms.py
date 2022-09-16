from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from . import models


class InscriptionForm(ModelForm):
    participant_type = forms.ChoiceField(
        choices=models.ParticipantType.choices,
        widget=forms.RadioSelect,
        label="Je suis :",
    )

    prefered_themes = forms.MultipleChoiceField(
        choices=models.Theme.choices,
        widget=forms.CheckboxSelectMultiple,
        label="Je choisis les thème sur lesquels je souhaite donner mon avis",
    )

    gives_gdpr_consent = forms.BooleanField(
        label="Je consens à l'utilisation de mes données personnelles",
    )

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
        fields = ["email", "first_name", "postal_code", "participant_type"]

    def save(self, commit=True):
        instance = super(InscriptionForm, self).save(commit=commit)
        preferred_themes = self.cleaned_data["prefered_themes"]
        for theme in preferred_themes:
            subscription = models.Subscription(participant_id=instance.id, theme=theme)
            subscription.save()
        return instance

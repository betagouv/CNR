from django import forms


class InscriptionForm(forms.Form):
    INTEREST_CHOICES = [
        ('education', 'Éducation'),
        ('sante', 'Santé'),
    ]
    PARTICIPANT_TYPE = [
        ('citoyen', 'Citoyen'),
        ('elu', 'Élu'),
        ('association', "Représentant d'une association" ),
    ]

    first_name = forms.CharField(label="Prénom")
    email = forms.EmailField(label="Courriel")
    postal_code = forms.RegexField(label="Code postal", regex="^[0-9]{1}[1-9]{1}[0-9]{3}$", max_length=5, min_length=5)
    prefered_themes = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=INTEREST_CHOICES,
        label="Thèmes favoris"
    )
    participant_type = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=PARTICIPANT_TYPE,
        label="Je suis:"
    )
    consent = forms.BooleanField(
        label="J'accepte que mes données soient traitées par gouv.fr conformément au RGPD.",
        required=True
    )

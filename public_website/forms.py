from django import forms


class FormulaireForm(forms.Form):
    INTEREST_CHOICES = [
        ('education', 'Éducation'),
        ('sante', 'Santé'),
        ('logement', 'Logement'),
        ('bien_viellir', 'Bien Viellir'),
        ('theme5', 'Theme 5'),
        ('theme6', 'Theme 6'),
    ]
    PARTICIPANT_TYPE = [
        ('citoyen', 'Citoyen'),
        ('elu', 'Élu'),
        ('participant_type', "Représentant d'une association" ),
    ]
    first_name = forms.CharField(label="Prénom")
    email = forms.EmailField(label="Courriel")
    postal_code = forms.RegexField(label="Code postal", regex="^[0-9]{1}[1-9]{1}[0-9]{3}$", max_length=5, min_length=5)
    prefered_themes = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=INTEREST_CHOICES,
        label="Thèmes favoris"
    )
    participant_type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=PARTICIPANT_TYPE,
        label="Qui êtes vous ?"
    )
    consent = forms.BooleanField(
        label="J'accepte que mes données soient traitées par gouv.fr conformément au RGPD.",
        required=True
    )


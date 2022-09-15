from django import forms


class FormulaireForm(forms.Form):
    INTEREST_CHOICES = [
        ('education', 'Éducation'),
        ('sante', 'Santé'),
        ('logement', 'Logement'),
        ('bien_viellir', 'Bien vieillir'),
        ('democratie', 'Démocratie'),
        ('theme6', 'Theme 6'),
    ]
    PARTICIPANT_TYPE = [
        ('citoyen', 'Citoyen'),
        ('elu', 'Élu'),
        ('participant_type', 'Association'),
    ]
    first_name = forms.CharField()
    email = forms.EmailField()
    postal_code = forms.RegexField(regex="^[0-9]{1}[1-9]{1}[0-9]{3}$", max_length=5, min_length=5)
    prefered_themes = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=INTEREST_CHOICES,
    )
    # TODO faire un radio button
    participant_type = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=PARTICIPANT_TYPE,
    )
    consent = forms.BooleanField(
        label="J'accepte que mes données soient traitées par gouv.fr conformément au RGPD.",
        required=True
    )

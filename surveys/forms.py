from django import forms

answer_types = {
    "ONE_TEXT_FIELD": (forms.CharField, 1),
    "THREE_TEXT_FIELD": (forms.CharField, 3),
    "FIVE_TEXT_FIELD": (forms.CharField, 5),
}


class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop("questions")
        super(SurveyForm, self).__init__(*args, **kwargs)

        for question in questions:
            field_length = answer_types[question.answer_type][1]
            for i in range(0, field_length):
                field_class = answer_types[question.answer_type][0]
                self.fields[f"{question.label}-{i}"] = field_class(
                    label=question.label, required=False
                )


class SelectSurveysForm(forms.Form):
    def __init__(self, surveys, *args, **kwargs):
        super(SelectSurveysForm, self).__init__(*args, **kwargs)
        self.fields["surveys"] = forms.MultipleChoiceField(
            choices=[(survey.label, survey) for survey in surveys],
            widget=forms.CheckboxSelectMultiple(),
        )

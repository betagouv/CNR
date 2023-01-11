from behave import then

from surveys.models import SurveyAnswer


@then('il existe une réponse "{}"')
def step_impl(context, answer):
    assert SurveyAnswer.objects.last().answer == answer

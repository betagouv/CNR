from behave import then

from public_website.models import Participant


@then('un participant existe avec l\'email "{}"')
def step_impl(context, email):
    assert Participant.objects.get(email=email)

from django.test import TestCase
from django.urls import resolve

from public_website import views


class TestCgu(TestCase):
    def test_cgu_url_calls_right_view(self):
        match = resolve("/cgu/")
        self.assertEqual(match.func, views.cgu_view)

    def test_cgu_url_calls_right_template(self):
        response = self.client.get("/cgu/")
        self.assertTemplateUsed(response, "public_website/cgu.html")

    def test_cgu_response_contains_welcome_message(self):
        response = self.client.get("/cgu/")
        self.assertContains(response, "Conditions générales d'utilisation")


class TestMentionsLegales(TestCase):
    def test_mentions_legales_url_calls_right_view(self):
        match = resolve("/mentions-legales/")
        self.assertEqual(match.func, views.mentions_legales_view)

    def test_mentions_legales_url_calls_right_template(self):
        response = self.client.get("/mentions-legales/")
        self.assertTemplateUsed(response, "public_website/mentions_legales.html")

    def test_mentions_legales_response_contains_welcome_message(self):
        response = self.client.get("/mentions-legales/")
        self.assertContains(response, "Mentions légales")


class TestAccessibilite(TestCase):
    def test_accessibilite_url_calls_right_view(self):
        match = resolve("/accessibilite/")
        self.assertEqual(match.func, views.accessibilite_view)

    def test_accessibilite_url_calls_right_template(self):
        response = self.client.get("/accessibilite/")
        self.assertTemplateUsed(response, "public_website/accessibilite.html")

    def test_accessibilite_response_contains_welcome_message(self):
        response = self.client.get("/accessibilite/")
        self.assertContains(response, "Accessibilité")


class TestConfidentialite(TestCase):
    def test_confidentialite_url_calls_right_view(self):
        match = resolve("/confidentialite/")
        self.assertEqual(match.func, views.confidentialite_view)

    def test_confidentialite_url_calls_right_template(self):
        response = self.client.get("/confidentialite/")
        self.assertTemplateUsed(response, "public_website/confidentialite.html")

    def test_confidentialite_response_contains_welcome_message(self):
        response = self.client.get("/confidentialite/")
        self.assertContains(response, "Politique de confidentialité")


class TestDSFR(TestCase):
    def test_dsfr_is_loaded(self):
        response = self.client.get("/cgu/")
        dsfr_proof = (
            '<link rel="stylesheet" href="/static/dsfr/dist/utility/icons/icons.css">'
        )
        self.assertContains(response, dsfr_proof)


class TestNoAdmin(TestCase):
    def test_admin_app_redirect(self):
        response = self.client.get("/admin")
        self.assertRedirects(
            response, "/admin/", status_code=301, fetch_redirect_response=False
        )

    def test_admin_app_with_slash_returns_404(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 404)


class TestPlanDuSite(TestCase):
    def test_plan_du_site_url_calls_right_view(self):
        match = resolve("/plan-du-site/")
        self.assertEqual(match.func, views.plan_du_site_view)

    def test_plan_du_site_url_calls_right_template(self):
        response = self.client.get("/plan-du-site/")
        self.assertTemplateUsed(response, "public_website/plan_du_site.html")

    def test_plan_du_site_response_contains_title(self):
        response = self.client.get("/plan-du-site/")
        self.assertContains(response, "Plan du site")

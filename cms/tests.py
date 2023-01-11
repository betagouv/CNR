from django.test import TestCase

from cms.factories import ContentPageFactory


class CMSPageTest(TestCase):
    fixtures = ["fixtures.json"]

    def test_title_tag_when_seo_title_is_set(self):
        page = ContentPageFactory(with_seo_title=True, with_search_description=True)
        response = self.client.get(f"/{ page.slug }/")
        self.assertContains(
            response,
            f"<title>{ page.seo_title } — Conseil National de la Refondation</title>",
            count=1,
            html=True,
        )

    def test_title_tag_when_seo_title_is_not_set(self):
        page = ContentPageFactory()
        response = self.client.get(f"/{ page.slug }/")
        self.assertContains(
            response,
            f"<title>{ page.title } — Conseil National de la Refondation</title>",
            count=1,
            html=True,
        )

    def test_meta_description_tag_when_search_description_is_set(self):
        page = ContentPageFactory(with_search_description=True)
        response = self.client.get(f"/{ page.slug }/")
        self.assertContains(
            response,
            f'<meta name="description" content="{ page.search_description }" />',
            count=1,
            html=True,
        )

    def test_meta_description_tag_when_search_description_is_not_set(self):
        page = ContentPageFactory()
        response = self.client.get(f"/{ page.slug }/")
        self.assertContains(
            response, '<meta name="description" content="" />', count=1, html=True
        )

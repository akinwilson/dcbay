from unittest import skip

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase


from store.models import Category, Product
from views import product_all


@skip("Demonstrating purposes")
class TestSkip(TestCase):
    def test_skip_example(self):
        pass


class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username="admin")
        Category.objects.create(name="cat_1", slug="cat_1_slug")
        Product.objects.create(
            category_id=1,
            title="testin cat title",
            created_by_id=1,
            slug="testin-cat-title-slug",
            price=11.11,
            image="default.png",
        )

    def test_url_allowed_hosts(self):
        """
        testing allowed hosts
        """
        # not allowed
        response = self.c.get("/", HTTP_HOST="noaddress.com")
        self.assertEqual(response.status_code, 400)  # will fail
        # allowed
        response = self.c.get("/", HTTP_HOST="neuropharma.co.uk")
        self.assertEqual(response.status_code, 200)  # should work

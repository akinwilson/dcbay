from django.test import TestCase

from store.models import Category


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(
            name="test_cat_cns", slug="test_cat_cns_slug"
        )

    def test_category_model_entry(self):
        """
        Testing category model data insertion types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

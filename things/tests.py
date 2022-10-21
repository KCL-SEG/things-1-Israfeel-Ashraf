from django.test import TestCase

from .models import Thing
from django.core.exceptions import ValidationError

# Create your tests here.
class ThingTestCase(TestCase):

    def setUp(self):

        self.thing = Thing.objects.create(
            name = "THING",
            description = "A random test string for the description",
            quantity = 10
        )


    def test_name_is_valid(self):

        self.thing.name = "a" * 30
        self._assert_thing_is_valid()

    def test_name_is_not_valid(self):

        self.thing.name = "a" * 31
        self._assert_thing_is_invalid()

    def test_name_is_unique(self):

        self.thing.name = "THING"

        thing2 = self._create_second_thing()
        thing2.name = "THING 2"

        self._assert_thing_is_valid()

    def test_name_is_not_unique(self):

        newThing = Thing.objects.create(
            name = "NEW THING",
            description = "Description",
            quantity = 3
        )

        self.thing.name = newThing.name
        self._assert_thing_is_invalid()

    def test_name_is_not_blank(self):

        self.name = 'NAMESTRING'
        self._assert_thing_is_valid()

    def test_name_is_blank(self):

        self.thing.name = ''
        self._assert_thing_is_invalid()

    def test_description_is_valid(self):
        self.thing.description = "a" * 120
        self._assert_thing_is_valid()

    def test_description_is_not_valid(self):
        self.thing.description = "a" * 121
        self._assert_thing_is_invalid()

    def test_description_need_not_be_unique(self):
        newThing = Thing.objects.create(
            name = "NEW THING",
            description = "A random test string for the description",
            quantity = 10
        )

        self.thing.description = newThing.description
        self._assert_thing_is_valid()

    def test_description_can_be_blank(self):
        self.thing.description = ''
        self._assert_thing_is_valid()

    def test_quantity_need_not_be_uniqie(self):
        newThing = Thing.objects.create(
            name = "NEW THING",
            description = "A random test string for the description",
            quantity = 12
        )
        self.thing.quantity = newThing.quantity
        self._assert_thing_is_valid()

    def test_quantity_cannont_be_less_than_zero(self):
        self.thing.quantity = -1
        self._assert_thing_is_invalid()

    def test_quantity_cannot_be_more_than_100(self):
        self.thing.quantity = 101
        self._assert_thing_is_invalid()

    def test_quantity_can_be_zero(self):
        self.thing.quantity = 0
        self._assert_thing_is_valid()

    def test_quantity_can_be_100(self):
        self.thing.quantity = 100
        self._assert_thing_is_valid()

    def _assert_thing_is_valid(self):

        try:
            self.thing.full_clean()

        except(ValidationError):
            self.fail('Test thing should be valid')

    def _assert_thing_is_invalid(self):

        with self.assertRaises(ValidationError):
            self.thing.full_clean()

    def _create_second_thing(self):

        thing = Thing.objects.create(
            name = "THING 2",
            description = "Another string for the description",
            quantity = 5
        )

        return thing

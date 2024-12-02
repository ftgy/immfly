from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase

from media_api.aux_funcs import create_content_channel, create_channel_with_subchannels, create_content
from media_api.models import Channel


class ModelTestCases(APITestCase):
    # Model tests
    def test_create_channel_with_contents(self):
        channel1 = create_content_channel(title="Channel 1")
        self.assertEqual(len(channel1.subcontents.all()), 1)

    def test_create_channel_with_subchannels(self):
        channel1 = create_channel_with_subchannels()
        self.assertEqual(len(channel1.subchannels.all()), 2)

    def test_create_empty_channel_should_fail(self):
        channel1 = Channel(title="Channel 1", language="en", picture_url="picture1.jpg")
        with self.assertRaises(ValidationError):
            channel1.save()

    def test_add_content_to_channel_with_subchanneles_should_fail(self):
        channel1 = create_channel_with_subchannels()
        content1 = create_content()
        channel1.subcontents.add(content1)
        with self.assertRaises(ValidationError):
            channel1.save()

    def test_add_channel_to_channel_with_subcontents_should_fail(self):
        channel1 = create_content_channel(title="Channel 1")
        channel2 = create_content_channel(title="Channel 2")
        channel1.subchannels.add(channel2)
        with self.assertRaises(ValidationError):
            channel1.save()

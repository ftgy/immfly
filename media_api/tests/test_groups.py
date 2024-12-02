from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from media_api.aux_funcs import create_content_channel
from media_api.models import Group, Channel


class ChannelGroupTestCase(APITestCase):
    def setUp(self):
        self.group1 = Group.objects.create(name="Group 1")
        self.group2 = Group.objects.create(name="Group 2")
        self.parent_channel = Channel(title="Parent", language="en", picture_url="/parent.jpg")
        self.parent_channel.save(skip_validations=True)
        self.parent_channel.groups.add(self.group1, self.group2)

    def test_channel_with_valid_groups(self):
        child_channel = create_content_channel("Child")
        child_channel.groups.add(self.group1)
        child_channel.save()

    def test_channel_with_invalid_groups(self):
        child_channel = create_content_channel("Child")
        child_channel.parent_channel = self.parent_channel
        child_channel.groups.add(Group.objects.create(name="Invalid Group"))
        with self.assertRaises(ValidationError):
            child_channel.save()

    def test_filter_channels_by_group(self):
        self.parent_channel.groups.add(self.group1)
        response = self.client.get('/channels/filter_by_group/?group=Group 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Parent")

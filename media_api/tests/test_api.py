import json

from rest_framework import status
from rest_framework.test import APITestCase

from media_api.aux_funcs import create_channel_with_subchannels


class ChannelAPITestCase(APITestCase):
    def setUp(self):
        self.channel1 = create_channel_with_subchannels()

    # Web API tests
    def test_list_channels(self):
        response = self.client.get('/channels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_channel_by_id(self):
        response = self.client.get(f'/channels/{self.channel1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Channel 1")

    def test_get_subchannels_by_channel(self):
        response = self.client.get(f'/channels/{self.channel1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['subchannels']), 2)

    def test_get_content_by_channel(self):
        channel2 = self.channel1.subchannels.first()
        response = self.client.get(f'/channels/{channel2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['subcontents']), 1)

    def test_get_subchannels_and_contents(self):
        response = self.client.get(f'/channels/{self.channel1.id}/subchannels_and_contents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('subchannels', [])), 2)
        self.assertEqual(len(response.json().get('subcontents', [])), 0)

        channel2 = self.channel1.subchannels.first()
        response = self.client.get(f'/channels/{channel2.id}/subchannels_and_contents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('subchannels', [])), 0)
        self.assertEqual(len(response.json().get('subcontents', [])), 1)

    def test_filter_channels_by_group(self):
        response = self.client.get('/channels/filter_by_group/?group=Test Group')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Channel 1")
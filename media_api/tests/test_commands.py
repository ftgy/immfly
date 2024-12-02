from decimal import Decimal

from django.test import TestCase
from django.core.management import call_command
from io import StringIO

from media_api.aux_funcs import create_content_channel, create_parent_channel
from media_api.models import Channel, Content, Group


class CalculateChannelRatingsCommandTest(TestCase):

    def setUp(self):
        # channel with two contents
        channel1 = create_content_channel("channel 1")
        content1 = channel1.subcontents.first()
        content1.rating = Decimal(2.0)
        content1.save()

        content2 = Content.objects.create(file_url="/a/b/c", rating=Decimal(4.0))
        channel1.subcontents.add(content2)

        # channel with one content
        channel2 = create_content_channel("channel 2")
        content3 = channel2.subcontents.first()
        content3.rating = Decimal(6.0)
        content3.save()

        # parent channel
        channel3 = create_parent_channel("channel 3")
        channel3.subchannels.add(channel1)
        channel3.subchannels.add(channel2)
        channel3.save()

    def test_command_creates_csv_file(self):
        # Run the management command and capture the output
        out = StringIO()
        call_command('calculate_channel_ratings', stdout=out)

        # Check if the CSV file was created
        with open('channel_ratings.csv', 'r', encoding='utf-8') as csvfile:
            content = csvfile.read()
            self.assertIn('Title,Avg Rating', content)
            self.assertIn('channel 3,4.50', content)
            self.assertIn('channel 2,6.00', content)
            self.assertIn('channel 1,3.00', content)

        # Clean up the CSV file after the test
        import os
        os.remove('channel_ratings.csv')

    def tearDown(self):
        # Clean up any objects created during the test
        Channel.objects.all().delete()
        Group.objects.all().delete()
        Content.objects.all().delete()

from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from media_api.models import Channel, Content, Group


class CalculateChannelRatingsCommandTest(TestCase):

    def setUp(self):
        # Create a group for channels
        self.group = Group.objects.create(name="Test Group")

        # Create a channel with contents
        self.channel1 = Channel(title="Channel 1", language="en", picture_url="channel1.jpg")
        self.channel1.save(skip_validations=True)

        self.channel1.groups.add(self.group)

        Content.objects.create(file_url="/a/b/c", rating=8.5, channel=self.channel1)
        Content.objects.create(file_url="/a/b/c", rating=7.5, channel=self.channel1)

        # Create a channel without contents
        self.channel2 = Channel(title="Channel 2", language="en", picture_url="channel2.jpg")
        self.channel2.save(skip_validations=True)

        self.channel2.groups.add(self.group)

        # Create a subchannel with contents
        self.subchannel = Channel(title="Subchannel 1", language="en", picture_url="subchannel1.jpg",
                                  parent_channel=self.channel1)
        self.subchannel.save(skip_validations=True)

        Content.objects.create(file_url="/a/b/c", rating=9.0, channel=self.subchannel)

    def test_command_creates_csv_file(self):
        # Run the management command and capture the output
        out = StringIO()
        call_command('calculate_channel_ratings', stdout=out)

        # Check if the CSV file was created
        with open('channel_ratings.csv', 'r', encoding='utf-8') as csvfile:
            content = csvfile.read()
            self.assertIn('Channel Title,Average Rating', content)  # Check header exists
            self.assertIn('Channel 1,8.0', content)  # Check data for channel with contents
            self.assertIn('Subchannel 1,9.0', content)  # Check data for subchannel with content
            self.assertIn('Channel 2,No rating available', content)  # Check data for channel with no content

        # Clean up the CSV file after the test
        import os
        os.remove('channel_ratings.csv')

    def tearDown(self):
        # Clean up any objects created during the test
        Channel.objects.all().delete()
        Group.objects.all().delete()
        Content.objects.all().delete()

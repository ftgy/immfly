import csv

from django.core.management import BaseCommand
from django.db.models import Avg

from media_api.models import Channel


class Command(BaseCommand):
    help = 'Calculates the average ratings of each channel and exports them to a CSV file.'

    def handle(self, *args, **kwargs):
        # Get all channels and calculate their average ratings
        channels = Channel.objects.all()
        channel_ratings = []

        for channel in channels:
            # Calculate average rating of the channel
            if channel.subcontents.exists():  # Only calculate if the channel has contents
                average_rating = channel.subcontents.aggregate(Avg('rating'))['rating__avg']
                channel_ratings.append((channel.title, average_rating))
            elif channel.subchannels.exists():  # Calculate based on subchannels if any
                # Recursively calculate the rating based on subchannels
                subchannel_ratings = []
                for subchannel in channel.subchannels.all():
                    if subchannel.subcontents.exists():
                        sub_avg_rating = subchannel.subcontents.aggregate(Avg('rating'))['rating__avg']
                        if sub_avg_rating is not None:
                            subchannel_ratings.append(sub_avg_rating)
                if subchannel_ratings:
                    average_rating = sum(subchannel_ratings) / len(subchannel_ratings)
                    channel_ratings.append((channel.title, average_rating))
                else:
                    channel_ratings.append((channel.title, None))  # Undefined rating

        # Sort by rating in descending order
        channel_ratings.sort(key=lambda x: x[1] if x[1] is not None else 0, reverse=True)

        # Write to CSV
        with open('channel_ratings.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Channel Title', 'Average Rating'])
            for title, rating in channel_ratings:
                if rating is not None:
                    writer.writerow([title, round(rating, 2)])
                else:
                    writer.writerow([title, 'No rating available'])

        self.stdout.write(self.style.SUCCESS('Ratings calculated and exported to channel_ratings.csv'))
import csv

from django.core.management import BaseCommand

from media_api.models import Channel


class Command(BaseCommand):
    help = 'Calculates the average ratings of each channel and exports them to a CSV file.'

    def handle(self, *args, **kwargs):
        # calculate ratings
        channel_ratings = calculate_ratings_for_all_channels()

        # sort by rating
        sorted_channels = dict(sorted(channel_ratings.items(), key=lambda item: item[1], reverse=True))

        # Write to CSV
        with open('channel_ratings.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Avg Rating'])
            for title, rating in sorted_channels.items():
                if rating is not None:
                    writer.writerow([title, round(rating, 2)])
                else:
                    writer.writerow([title, 'No rating available'])

        self.stdout.write(self.style.SUCCESS('Ratings calculated and exported to channel_ratings.csv'))


def calculate_channel_rating(channel):
    """
    Recursively calculates the rating for a channel based on its contents or subchannels.

    Args:
        channel (Channel): The channel object.

    Returns:
        float: The average rating of the channel or None if no rating can be calculated.
    """
    subchannels = channel.subchannels.all()  # Assume a related_name for subchannels
    contents = channel.subcontents.all()  # Assume a related_name for contents

    if subchannels.exists():
        # Recursively calculate the ratings of subchannels
        subchannel_ratings = [
            calculate_channel_rating(subchannel) for subchannel in subchannels
        ]
        # Filter out None ratings from undefined subchannels
        valid_ratings = [rating for rating in subchannel_ratings if rating is not None]
        return sum(valid_ratings) / len(valid_ratings) if valid_ratings else None

    elif contents.exists():
        # Calculate the average rating of the contents
        total_rating = sum(content.rating for content in contents)
        return total_rating / contents.count()

    # No subchannels or contents, rating is undefined
    return None


def calculate_ratings_for_all_channels():
    """
    Calculates and prints the ratings for all channels in the database.

    Returns:
        dict: A dictionary mapping channel titles to their average ratings.
    """
    channel_ratings = {}
    all_channels = Channel.objects.all()

    for channel in all_channels:
        rating = calculate_channel_rating(channel)
        channel_ratings[channel.title] = rating

    return channel_ratings

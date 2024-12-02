from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg


class Group(models.Model):
    name = models.CharField(max_length=255)


class Content(models.Model):
    file_url = models.URLField()
    metadata = models.JSONField(null=True)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('10.0'))],
        help_text="Rating must be a decimal between 1.0 and 10.0."
    )
    channel = models.ForeignKey("Channel", null=True, blank=True, related_name='subcontents', on_delete=models.CASCADE)

    def clean(self):
        if self.channel and self.channel.subchannels.exists():
            raise ValidationError("Cannot add content to a channel that has subchannels.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Channel(models.Model):
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=10)
    picture_url = models.URLField()
    parent_channel = models.ForeignKey('self', null=True, blank=True, related_name='subchannels',
                                       on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)

    def clean(self):
        has_subchannels = self.subchannels.exists()
        has_subcontents = self.subcontents.exists()

        if has_subchannels and has_subcontents:
            raise ValidationError("A channel cannot have both subchannels and contents.")
        if not has_subchannels and not has_subcontents:
            raise ValidationError("A channel must have either subchannels or contents.")

    def save(self, *args, **kwargs):
        skip_validations = kwargs.pop("skip_validations", None)
        super().save(*args, **kwargs)
        if not skip_validations:
            self.clean()

    # def average_rating(self):
    #     if self.subchannels.exists():
    #         subchannel_ratings = [sub.average_rating() for sub in self.subchannels.all() if
    #                               sub.average_rating() is not None]
    #         return sum(subchannel_ratings) / len(subchannel_ratings) if subchannel_ratings else None
    #     elif self.contents.exists():
    #         return self.contents.aggregate(Avg('rating'))['rating__avg']
    #     return None

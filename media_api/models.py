from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from rest_framework.exceptions import ValidationError


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
        super().clean()
        self.validate_subcontents_subchannels()
        self.validate_groups()

    def save(self, *args, **kwargs):
        skip_validations = kwargs.pop("skip_validations", None)
        super().save(*args, **kwargs)
        if not skip_validations:
            self.clean()

    def validate_subcontents_subchannels(self):
        has_subchannels = self.subchannels.exists()
        has_subcontents = self.subcontents.exists()

        if has_subchannels and has_subcontents:
            raise ValidationError("A channel cannot have both subchannels and contents.")
        if not has_subchannels and not has_subcontents:
            raise ValidationError("A channel must have either subchannels or contents.")

    def validate_groups(self):
        if self.parent_channel:
            parent_groups = set(self.parent_channel.groups.all())
            current_groups = set(self.groups.all())
            if not current_groups.issubset(parent_groups):
                raise ValidationError("A channel's groups must be a subset of its parent's groups.")

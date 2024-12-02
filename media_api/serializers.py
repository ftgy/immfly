from rest_framework import serializers

from media_api.models import Content, Channel


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    subchannels = serializers.SerializerMethodField()
    subcontents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = '__all__'

    def get_subchannels(self, obj):
        if obj.subchannels.exists():
            return ChannelSerializer(obj.subchannels.all(), many=True).data
        return []

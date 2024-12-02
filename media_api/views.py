from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from media_api.models import Channel, Group
from media_api.serializers import ChannelSerializer, ContentSerializer


@api_view(['GET'])
def list_channels(request):
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_channel_by_id(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    serializer = ChannelSerializer(channel)
    return Response(serializer.data)


@api_view(['GET'])
def get_subchannels_and_contents(request, pk):
    channel = get_object_or_404(Channel, pk=pk)

    if channel.subchannels.exists():
        subchannels = Channel.objects.filter(parent_channel=channel)

        data = {
            'subchannels': ChannelSerializer(subchannels, many=True).data,
        }
        return JsonResponse(data)

    elif channel.subcontents.exists():
        subcontents = channel.subcontents.all()

        data = {
            'subcontents': ContentSerializer(subcontents, many=True).data
        }
        return JsonResponse(data)

    else:
        raise ValidationError()


@api_view(['GET'])
def filter_channels_by_group(request):
    group_name = request.query_params.get('group')
    if not group_name:
        return Response({'error': 'Group name is required'}, status=status.HTTP_400_BAD_REQUEST)

    group = Group.objects.filter(name=group_name).first()
    if not group:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    channels = Channel.objects.filter(groups=group)
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)

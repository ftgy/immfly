from media_api.models import Content, Channel


def create_content():
    content1 = Content(file_url="/a/b/c", rating=8.0, metadata={"a": "a"})
    content1.save()
    return content1


def create_content_channel(title):
    content1 = Content(file_url="/a/b/c", rating=8.0, metadata={"a": "a"})
    content1.save()
    content_channel = Channel(title=title, language="en", picture_url="picture1.jpg")
    content_channel.save(skip_validations=True)
    content_channel.subcontents.add(content1)
    content_channel.save()

    return content_channel


def create_parent_channel(title):
    parent_channel = Channel(title=title, language="en", picture_url="picture1.jpg")
    parent_channel.save(skip_validations=True)
    return parent_channel


def create_channel_with_subchannels():
    channel1 = create_parent_channel(title="Channel 1")
    channel2 = create_content_channel(title="Channel 2")
    channel2.parent_channel = channel1
    channel2.save()
    channel3 = create_content_channel(title="Channel 3")
    channel3.parent_channel = channel1
    channel3.save()
    return channel1

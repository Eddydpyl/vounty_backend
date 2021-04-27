from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework import serializers
from urllib import parse

from api.models import User, Tag, Vote, Vounty, Entry, Comment, Fund
from vounty_backend.settings import GS_BUCKET_NAME


class ImageSerializerField(serializers.Field):

    def to_representation(self, value):
        if not value: return None
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(value.url)
        return value.url

    def to_internal_value(self, data):
        try:
            URLValidator(data)
            url = parse.unquote(data)
            path = 'https://storage.googleapis.com/' + GS_BUCKET_NAME + '/'
            if url.startswith(path):
                return url[len(path):]
            raise ValueError()
        except ValidationError as e:
            return data


class UserSerializer(serializers.ModelSerializer):
    image = ImageSerializerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'image', 'about']
        extra_kwargs = {
            'password': {'write_only': True},
            'image': {'required': False},
            'about': {'required': False}
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'text']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'user', 'content_type', 'object_id', 'content_object', 'date', 'like']
        read_only_fields = ['date']
        extra_kwargs = {
            'content_type': {'write_only': True},
            'object_id': {'write_only': True}
        }


class VountySerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    image = ImageSerializerField()

    class Meta:
        model = Vounty
        fields = ['id', 'user', 'title', 'subtitle', 'description',
                  'image', 'featured', 'fund_count', 'date', 'prize', 'tags']
        read_only_fields = ['featured', 'fund_count', 'date', 'prize', 'tags']
        extra_kwargs = {
            'description': {'required': False},
            'image': {'required': False}
        }


class EntrySerializer(serializers.ModelSerializer):
    votes = VoteSerializer(read_only=True, many=True)

    class Meta:
        model = Entry
        fields = ['id', 'user', 'vounty', 'votes', 'vote_count', 'granted', 'date', 'text']
        read_only_fields = ['votes', 'vote_count', 'granted', 'date']


class CommentSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'vounty', 'votes', 'vote_count', 'date', 'text']
        read_only_fields = ['votes', 'vote_count', 'date']


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ['id', 'user', 'vounty', 'date', 'amount', 'charge']
        read_only_fields = ['date']
        extra_kwargs = {
            'charge': {'required': False}
        }

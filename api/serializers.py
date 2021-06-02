from rest_framework import serializers

from api.models import User, Tag, Vote, Vounty, Entry, Comment, Fund, Subscription
from api.utils import handle_image


class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)


class ImageSerializerField(serializers.Field):

    def to_representation(self, value):
        if not value: return None
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(value.url)
        return value.url

    def to_internal_value(self, data):
        return handle_image(data)


class UserSerializer(serializers.ModelSerializer):
    image = ImageSerializerField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'image', 'about']
        extra_kwargs = {
            'email': {'write_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'text']


class VoteSerializer(serializers.ModelSerializer):
    user = RelatedFieldAlternative(queryset=User.objects.all(), serializer=UserSerializer)

    class Meta:
        model = Vote
        fields = ['id', 'user', 'date', 'like']
        read_only_fields = ['date']


class VountySerializer(serializers.ModelSerializer):
    user = RelatedFieldAlternative(queryset=User.objects.all(), serializer=UserSerializer)
    tags = TagSerializer(read_only=True, many=True)
    image = ImageSerializerField(required=False)

    class Meta:
        model = Vounty
        fields = ['id', 'user', 'title', 'subtitle', 'description',
                  'image', 'featured', 'comment_count', 'entry_count',
                  'fund_count', 'date', 'prize', 'reddit', 'tags']
        read_only_fields = ['featured', 'comment_count', 'entry_count',
                            'fund_count', 'date', 'prize', 'reddit', 'tags']
        optional_fields = ['description', 'image']


class CommentSerializer(serializers.ModelSerializer):
    user = RelatedFieldAlternative(queryset=User.objects.all(), serializer=UserSerializer)
    vounty = RelatedFieldAlternative(queryset=Vounty.objects.all(), serializer=VountySerializer)
    votes = VoteSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'vounty', 'votes', 'vote_count', 'date', 'text']
        read_only_fields = ['votes', 'vote_count', 'date']


class EntrySerializer(serializers.ModelSerializer):
    user = RelatedFieldAlternative(queryset=User.objects.all(), serializer=UserSerializer)
    vounty = RelatedFieldAlternative(queryset=Vounty.objects.all(), serializer=VountySerializer)
    votes = VoteSerializer(read_only=True, many=True)

    class Meta:
        model = Entry
        fields = ['id', 'user', 'vounty', 'votes', 'vote_count', 'granted', 'date', 'text']
        read_only_fields = ['votes', 'vote_count', 'granted', 'date']


class FundSerializer(serializers.ModelSerializer):
    user = RelatedFieldAlternative(queryset=User.objects.all(), serializer=UserSerializer)
    vounty = RelatedFieldAlternative(queryset=Vounty.objects.all(), serializer=VountySerializer)

    class Meta:
        model = Fund
        fields = ['id', 'user', 'vounty', 'date', 'amount', 'charge']
        read_only_fields = ['date']
        optional_fields = ['charge']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = RelatedFieldAlternative(queryset=User.objects.all(), serializer=UserSerializer)
    vounty = RelatedFieldAlternative(queryset=Vounty.objects.all(), serializer=VountySerializer)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'vounty', 'new_comment', 'new_entry', 'new_fund']

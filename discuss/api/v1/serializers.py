from django.contrib.humanize.templatetags import humanize

from rest_framework import serializers

from ...models import Discuss


class DiscussSerializerRelation(serializers.ModelSerializer):
    humanize_time = serializers.SerializerMethodField(required=False)
    children_count = serializers.IntegerField(read_only=True)
    descendant_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Discuss
        fields = "__all__"

    def get_humanize_time(self, obj):
        return humanize.naturaltime(obj.created)


class DiscussSerializer(serializers.ModelSerializer):
    # parent = DiscussSerializerRelation(many=False)
    # children = DiscussSerializerRelation(many=True)
    children_count = serializers.IntegerField(read_only=True)
    descendant_count = serializers.IntegerField(read_only=True)
    humanize_time = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Discuss
        exclude = ["application"]

    def get_humanize_time(self, obj):
        return humanize.naturaltime(obj.created)


class DiscussCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create a new discuss
    """

    class Meta:
        model = Discuss
        fields = ["object_id", "parent", "content"]

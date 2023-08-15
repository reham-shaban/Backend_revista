from rest_framework import serializers

from main.models import  Topic, TopicFollow

# app stats and demographics

class AgeSerializer(serializers.Serializer):
    label = serializers.CharField()
    data = serializers.IntegerField()

class GenderSerializer(serializers.Serializer):
    label = serializers.CharField()
    data = serializers.IntegerField()


class TrendingTopicsSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='name')
    data = serializers.IntegerField(source='follower_count')

    class Meta:
        model = Topic
        fields = [ 'label', 'data']

    def get_follower_count(self, obj):
        return obj.topicfollow_set.count()
    


class TopicsActivitySerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='name')
    data = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['label', 'data']

    def get_data(self, obj):
        return obj.post_set.count()


class TopicsFollowingTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicFollow
        fields = ['id', 'profile', 'topic','created_at']
        read_only_fields = ['profile']
        

class TopicsFollowingsStatsSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    followers = serializers.IntegerField()
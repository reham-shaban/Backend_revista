from rest_framework import serializers

from .models import Topic, TopicFollow

# Topic
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'image']
        
# Topic Follow
class TopicFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicFollow
        fields = ['id', 'profile', 'topic']
        read_only_fields = ['profile']

    # def create(self, validated_data):
    #     user = self.context['request'].user  # Get the authenticated user
    #     profile = user.profile  # Get the Profile object of the authenticated user
    #     validated_data['profile'] = profile  # Assign the profile to the validated data
    #     return super().create(validated_data)
   

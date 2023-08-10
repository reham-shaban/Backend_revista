from django.shortcuts import get_object_or_404
from rest_framework import serializers
from chat.models import Chat
from accounts.models import CustomUser
from ..models import Report, Warn

# Report
class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.ReadOnlyField(source='get_reporter')
    reported_user = serializers.PrimaryKeyRelatedField(
       queryset=CustomUser.objects.all(), 
       required=False
    )
    reported_chat = serializers.PrimaryKeyRelatedField(
        queryset=Chat.objects.all(),  # Adjust the queryset according to your Chat model
        required=False,
    )

    class Meta:
        model = Report
        fields = ['reporter', 'type', 'category', 'reported_user', 'reported_post', 'reported_chat',
                  'description', 'status', 'moderator', 'moderator_comment', 'created_at' , 'updated_at']
        
    def create(self, validated_data):
        report_type = validated_data.get('type')
        reported_chat = validated_data.get('reported_chat')
        reported_post = validated_data.get('reported_post')
        reported_user = validated_data.get('reported_user')
        auth_user = self.context['request'].user
        
        if report_type == 'chat':
            if reported_chat is None:
                raise serializers.ValidationError("reported_chat is required for 'chat' reports.")
            user1 = reported_chat.user1
            user2 = reported_chat.user2
            if auth_user == user1:
                validated_data['reported_user'] = user2
            else:
                validated_data['reported_user'] = user1
                
        elif report_type == 'post':
            if reported_post is None:
                raise serializers.ValidationError("reported_post is required for 'post' reports.")
            user = reported_post.author.user 
            validated_data['reported_user'] = user
          
        elif not reported_user:
            raise serializers.ValidationError("reported_user is required.")

        report = Report.objects.create(
        **validated_data,
        reporter = auth_user,
        )
        return report

# Warn
class WarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warn
        fields = '__all__'
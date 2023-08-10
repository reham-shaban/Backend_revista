from rest_framework import serializers
from ..models import Report, Warn

# Report
class ReportSerializer(serializers.ModelSerializer):
     reporter = serializers.ReadOnlyField(source='get_reporter')

     class Meta:
        model = Report
        fields = ['reporter', 'type', 'category', 'reported_user', 'reported_post',
                  'description', 'status', 'moderator', 'moderator_comment', 'created_at' , 'updated_at']
        
     def create(self, validated_data):
          report = Report.objects.create(
          **validated_data,
          reporter_id=self.context['request'].user.id,
          )
          return report

# Warn
class WarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warn
        fields = '__all__'
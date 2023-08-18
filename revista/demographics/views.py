from django.shortcuts import render
from accounts.models import CustomUser
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import calendar
from .serializers import AgeSerializer, GenderSerializer, TrendingTopicsSerializer, TopicsActivitySerializer, TopicsFollowingsStatsSerializer
from rest_framework import generics 
from datetime import datetime
import json  
from main.models import Topic, TopicFollow

# Create your views here.

#App Statistics and Demographics
class AgeView(LoginRequiredMixin, PermissionRequiredMixin,generics.ListAPIView):
#class AgeView(generics.ListAPIView):#test
    permission_required = 'report.view_report'
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        current_year = timezone.now().year
        age_annotation = current_year - ExtractYear('birth_date')
        queryset = super().get_queryset()
        queryset = queryset.annotate(age=age_annotation)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        age_data = []
        age_ranges = [(0, 18), (19, 30), (31, 45), (46, 60), (61, 100)]
        
        for age_range in age_ranges:
            lower, upper = age_range
            count = queryset.filter(age__range=(lower, upper)).count()
            age_data.append({
                'label': f'{lower}-{upper}',
                'data': count
            })
        return render(request, 'demographics/age_stats.html', {'age_data': age_data})


#Gender
class GenderView(LoginRequiredMixin, PermissionRequiredMixin,generics.ListAPIView):#test
    permission_required = 'report.view_report'
    queryset = CustomUser.objects.all()
    serializer_class = GenderSerializer
    def get(self, request, *args, **kwargs):
        gender_distribution = CustomUser.objects.values('gender').annotate(count=Count('id'))

        gender_data = []
        for entry in gender_distribution:
            label = entry['gender']
            if label is None:
                label = "N/A"
            elif label == "M":
                label="Male"
            elif label == "F":
                label="Female"
            gender_data.append({
                'label': label,
                'data': entry['count']
            })

        return render(request, 'demographics/gender_stats.html', {'gender_data': gender_data})




class TrendingTopicsView(LoginRequiredMixin, PermissionRequiredMixin,generics.ListAPIView):
    permission_required = 'report.view_report'
    queryset = Topic.objects.annotate(follower_count=Count('topicfollow')).order_by('-follower_count')
    serializer_class = TrendingTopicsSerializer
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        topic_data = serializer.data  # Serialized data

        return render(request, 'demographics/trending_topics_stats.html', {'topic_data': json.dumps(topic_data)})
    

class TopicsActivityView(LoginRequiredMixin, PermissionRequiredMixin,generics.ListAPIView):
    permission_required = 'report.view_report'
    queryset = Topic.objects.annotate(post_count=Count('post')).order_by('-post_count')
    serializer_class = TopicsActivitySerializer
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        topic_data = serializer.data  # Serialized data

        return render(request, 'demographics/topics_activity_stats.html', {'topic_data': json.dumps(topic_data)})




class TopicsFollowingsStatsView(LoginRequiredMixin, PermissionRequiredMixin,generics.ListAPIView):
    serializer_class = TopicsFollowingsStatsSerializer
    permission_required = 'report.view_report'

    def get(self, request, *args, **kwargs):
        # Get URL parameters
        year = int(request.query_params.get('year', datetime.now().year))
        topic_id = int(request.query_params.get('topic', 1))

        current_year = datetime.now().year
        current_month = datetime.now().month

        # Create a dictionary to store follower counts for each month
        follower_counts = {month_num: 0 for month_num in range(1, 13)}

        queryset = TopicFollow.objects.filter(
            topic_id=topic_id,
            created_at__year=year
        ).annotate(
            month=ExtractMonth('created_at')
        ).values(
            'month'
        ).annotate(
            followers=Count('id')
        ).order_by('month')

        # Populate follower counts dictionary
        for entry in queryset:
            month_num = entry['month']
            follower_counts[month_num] = entry['followers']

        # If the year is the current year, only include months up to the current month
        if year == current_year:
            follower_counts = {month_num: count for month_num, count in follower_counts.items() if month_num <= current_month}

        # Create a list of dictionaries for each month
        month_names = [calendar.month_name[month_num] for month_num in range(1, 13)]
        result = [{'month': month_names[month_num-1], 'followers': count} for month_num, count in follower_counts.items()]
        topic_names = Topic.objects.values_list('name', flat=True)  

        context = {
            'topic_data': json.dumps(result),
            'topic_names': topic_names,
        }

        return render(request, 'demographics/topics_following_stats.html', context)

from datetime import datetime
import json  
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from knox.auth import TokenAuthentication
from rest_framework.exceptions import ValidationError
from .models import Profile, Topic, TopicFollow, Follow,Block
from .serializers import ProfileSerializer, VistorProfileSerializer, TopicSerializer, TopicFollowSerializer, FollowSerializer, FollowingListSerializer, FollowersListSerializer, BlockSerializer, BlockedListSerializer, AgeSerializer, GenderSerializer, TrendingTopicsSerializer, TopicsActivitySerializer, TopicsFollowingsStatsSerializer
from accounts.models import CustomUser
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from calendar import month_name
import calendar



# Profile
# List all Profiles
class ProfileView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

# Update My Profile [GET, PATCH]
class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile

# Retrieve single Profile with id
class SingleProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = VistorProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Topics
# List Topics
class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Follow Topics [GET, POST]
class TopicFollowView(generics.ListCreateAPIView):
    serializer_class = TopicFollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TopicFollow.objects.filter(profile__user=user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        profile = user.profile
        serializer.save(profile=profile)

class TopicUnFollowView(generics.DestroyAPIView):
    queryset = TopicFollow.objects.all()
    serializer_class = TopicFollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# Follow
# Follow someone [POST]
class FollowView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(follower=self.request.user.profile)

# UnFollow someone [DELETE]
class UnFollowView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

# List my following [GET]
class FollowingListView(generics.ListAPIView):
    serializer_class = FollowingListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Follow.objects.all()
        profile=self.request.user.profile
        queryset = queryset.filter(follower=profile)
        blocked = Block.objects.filter(blocker=profile).values_list('blocked', flat=True)
        blocked_by=Block.objects.filter(blocked=profile).values_list('blocker', flat=True)
        queryset = queryset.exclude(followed__id__in=blocked)
        queryset = queryset.exclude(followed__id__in=blocked_by)
        return queryset 
        
# List my followers [GET]
class FollowersListView(generics.ListAPIView):
    serializer_class = FollowersListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile=self.request.user.profile
        queryset = Follow.objects.all()
        queryset = queryset.filter(followed=self.request.user.profile)
        blocked = Block.objects.filter(blocker=profile).values_list('blocked', flat=True)
        blocked_by=Block.objects.filter(blocked=profile).values_list('blocker', flat=True)
        queryset = queryset.exclude(follower__id__in=blocked)
        queryset = queryset.exclude(follower__id__in=blocked_by)  
        return queryset
    
    
# List Blocked users
class BlockedUsers(generics.ListAPIView):
    serializer_class=BlockedListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=Block.objects.all()
        queryset=queryset.filter(blocker=self.request.user.profile)
        return queryset
    

class BlockUsers(generics.CreateAPIView):
    queryset = Block.objects.all()
    serializer_class=BlockSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        
        blocker = self.request.user.profile
        blocked = serializer.validated_data['blocked']
        
        if Block.objects.filter(blocker=blocker, blocked=blocked).exists():
            raise ValidationError("User already blocked.")
        
        serializer.save(blocker=blocker)


class UnblockUsers(generics.DestroyAPIView):
    queryset = Block.objects.all()
    serializer_class=BlockSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


#App Statistics and Demographics
# class AgeView(LoginRequiredMixin, PermissionRequiredMixin,generics.ListAPIView):
class AgeView(generics.ListAPIView):#test
    #permission_required = 'main.view_age_stats'
    queryset = CustomUser.objects.all()
    #serializer_class = AgeSerializer

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
        return render(request, 'main/age_stats.html', {'age_data': age_data})


#Gender
class GenderView(generics.ListAPIView):#test
    #permission_required = 'main.view_gender_stats'
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

        return render(request, 'main/gender_stats.html', {'gender_data': gender_data})

# class TrendingTopicsView(LoginRequiredMixin, PermissionRequiredMixin,generics.ListAPIView):
class TrendingTopicsView(generics.ListAPIView):#test
    #permission_required = 'main.view_trending_topics_stats'
    queryset = Topic.objects.annotate(follower_count=Count('topicfollow')).order_by('-follower_count')
    serializer_class = TrendingTopicsSerializer
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        topic_data = serializer.data  # Serialized data

        return render(request, 'main/trending_topics_stats.html', {'topic_data': json.dumps(topic_data)})
    

# class TopicsActivityView(LoginRequiredMixin, PermissionRequiredMixin,generics.ListAPIView):
class TopicsActivityView(generics.ListAPIView):#test
    #permission_required = 'main.view_topics_activity_stats'
    queryset = Topic.objects.annotate(post_count=Count('post')).order_by('-post_count')
    serializer_class = TopicsActivitySerializer
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        topic_data = serializer.data  # Serialized data

        return render(request, 'main/topics_activity_stats.html', {'topic_data': json.dumps(topic_data)})

class TopicsFollowingsStatsView(generics.ListAPIView):#test
    serializer_class = TopicsFollowingsStatsSerializer

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
        topic_names = Topic.objects.values_list('name', flat=True)  # Assuming 'name' is the field for topic names

        context = {
            'topic_data': json.dumps(result),
            'topic_names': topic_names,
        }

        return render(request, 'main/topics_following_stats.html', context)
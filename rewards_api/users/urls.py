from django.urls import path
from .views import user_profile, RewardLogListView, RewardRequestView

urlpatterns = [
    path("api/profile/", user_profile, name="user_profile"),
    path("api/rewards/", RewardLogListView.as_view(), name="reward-log-list"),
    path("api/rewards/request/", RewardRequestView.as_view(), name="reward-request"),
]

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^ht/', include('health_check.urls')),

    path('me/user/', views.current_user),
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetails.as_view()),

    path('tag/', views.TagList.as_view()),
    path('tag/<int:pk>/', views.TagDetails.as_view()),

    path('vote/', views.VoteList.as_view()),
    path('vote/<int:pk>/', views.VoteDetails.as_view()),

    path('vounty/', views.VountyList.as_view()),
    path('vounty/<int:pk>/', views.VountyDetails.as_view()),
    path('vounty/start/', views.start_vounty),
    path('vounty/fund/', views.fund_vounty),

    path('entry/', views.EntryList.as_view()),
    path('entry/<int:pk>/', views.EntryDetails.as_view()),
    path('entry/vote/', views.vote_entry),

    path('comment/', views.CommentList.as_view()),
    path('comment/<int:pk>/', views.CommentDetails.as_view()),
    path('comment/vote/', views.vote_comment),

    path('fund/', views.FundList.as_view()),
    path('fund/<int:pk>/', views.FundDetails.as_view()),

    path('subscription/', views.SubscriptionList.as_view()),
    path('subscription/<int:pk>/', views.SubscriptionDetails.as_view()),

    path('storage/', views.storage_url),
]

admin.site.enable_nav_sidebar = False

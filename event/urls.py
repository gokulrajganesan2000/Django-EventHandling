from django.urls import path
from . import views
from .views import UserPostedEventView,EventListView,EventDetailView#,EventUpdateView,EventDeleteView

urlpatterns = [
    path('',EventListView.as_view(),name='home-page' ),
    path('user/<str:username>',UserPostedEventView.as_view(),name='user-post-page' ),
    path('event/<int:pk>/',EventDetailView.as_view(),name='event-detail' ),
    #path('post/<int:pk>/update/', EventUpdateView.as_view(), name='post-update'),
    #path('post/<int:pk>/delete/', EventDeleteView.as_view(), name='post-delete'),
    path('about/',views.about,name='about-page' ),
    path('post_event/',views.post_event,name='post_event-page' ),
    path('principal_decision/<int:id>/',views.principal_decision,name='principal-decision-page' ),
    path('change_time/<int:id>/',views.change_time,name='change-time-page' ),
    path('requests/',views.requests,name='requests-page' ),
    path('accepted/',views.accepted,name='accepted-page' ),
    path('declined/',views.declined,name='declined-page' ),
    path('event_edit/<int:id>/',views.edit_event,name='event_edit-page' ),
]
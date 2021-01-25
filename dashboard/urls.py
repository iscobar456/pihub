from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.index),
    path('social', views.social),
    path('personal', views.personal),
    path('personal/<str:action>', views.personal),
    path('account', views.Account.as_view()),
    path('update-notes', views.update_notes),
    path('add-friend', views.add_friend),
    path('remove-friend/<int:friend_id>', views.remove_friend),
    path('profile-card/<int:friend_id>', views.get_profile_card)
]

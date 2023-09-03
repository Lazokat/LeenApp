from django.urls import path
from .views import (all_profiles,SignUp,search,home,PostCreate,PostDetail,
                    PostUpdate,Post_delete,PostList,post_like,Profile_detail,follow_system,Delete,ProfileCreate,
                    CreateThread,ListThreads,ThreadView,CreateMessage)
app_name='leena'
urlpatterns=[path('all/',all_profiles,name='all_profile'),
             path('signup/',SignUp.as_view(),name='signup'),
             path('search/',search,name='search_q'),
             path('home/',home,name='home'),
             path('create/', PostCreate.as_view(), name='post_create'),
             path('detail/<int:pk>',PostDetail.as_view(),name='post_detail'),
             path('<int:pk>/update/',PostUpdate.as_view(),name='post_update'),
             path('<int:pk>/delete/',Post_delete.as_view(),name='post_delete'),
             path('<int:pk>/like/',post_like,name='post_likes'),
             path('<int:pk>/follow/',follow_system,name='profile_follows'),
             path('profile/<int:pk>/', Profile_detail.as_view(), name='my_profile'),
             path('',PostList.as_view(),name='all_post'),
             path('delete/<int:pk>/',Delete.as_view(),name='delete_account'),
             path('profile_create/',ProfileCreate.as_view(),name='profile_create'),
            path('inbox/', ListThreads.as_view(), name='inbox'),
            path('inbox/create-thread', CreateThread.as_view(), name='create-thread'),
            path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
            path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),
             ]
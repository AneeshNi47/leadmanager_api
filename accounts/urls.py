from django.urls import path, include
from .api import NonSuperUsersApi, RegisterApi, LoginApi, UserApi, GroupListApi, GroupDetailApi, AddUserToGroupApi, RemoveUserFromGroupApi, ListUsersInGroupApi
from knox import views as knox_views

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterApi.as_view()),
    path('api/auth/login', LoginApi.as_view()),
    path('api/auth/user', UserApi.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    # Group endpoints
    path('api/groups', GroupListApi.as_view(), name='group-list'),
    path('api/groups/<int:pk>', GroupDetailApi.as_view(), name='group-detail'),
    path('api/groups/add_user', AddUserToGroupApi.as_view(), name='add-user-to-group'),
    path('api/groups/remove_user', RemoveUserFromGroupApi.as_view(), name='remove-user-from-group'),
    path('api/groups/<int:group_id>/users', ListUsersInGroupApi.as_view(), name='list-users-in-group'),
    # User Endpoints
    path('api/auth/non_super_users', NonSuperUsersApi.as_view({'get': 'list'}), name='non-super-users-list'),
]

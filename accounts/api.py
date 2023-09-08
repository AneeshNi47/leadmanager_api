from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, GroupSerializer, GroupUserListSerializer

# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Get User API
class UserApi(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# Group List API
class GroupListApi(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

# Group Detail API
class GroupDetailApi(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# Add User to Group API
class AddUserToGroupApi(generics.CreateAPIView):
    serializer_class = GroupUserListSerializer

    def post(self, request, *args, **kwargs):
        group_id = request.data.get('group_id')
        user_id = request.data.get('user_id')

        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)

        group.user_set.add(user)

        return Response({"message": "User added to group"}, status=status.HTTP_200_OK)

# Remove User from Group API
class RemoveUserFromGroupApi(generics.DestroyAPIView):
    serializer_class = GroupUserListSerializer

    def delete(self, request, *args, **kwargs):
        group_id = request.data.get('group_id')
        user_id = request.data.get('user_id')

        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)

        group.user_set.remove(user)

        return Response({"message": "User removed from group"}, status=status.HTTP_200_OK)

# List Users in Group API
class ListUsersInGroupApi(generics.ListAPIView):
    serializer_class = GroupUserListSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group = Group.objects.get(id=group_id)
        return group.user_set.all()

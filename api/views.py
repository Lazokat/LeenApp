from rest_framework import viewsets
from Main1.models import CustomModel,Post,Profile,Comment,ThreadModel,MessageModel
from .serializers import PostSerializer,ProfileSerializer,CommentSerializer,CustomModelSerializer,ThreadSerializer,MessageSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import AuthorOrRead
class CustomViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CustomModel.objects.all()
    serializer_class = CustomModelSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrRead,)
    queryset = Post.objects.all()
    serializer_class =PostSerializer

class ProfileViewset(viewsets.ModelViewSet):
    permission_classes =(AuthorOrRead,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CommentViewset(viewsets.ModelViewSet):
    permission_classes =(AuthorOrRead,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
class ThreadViewset(viewsets.ModelViewSet):
    permission_classes =(AuthorOrRead,)
    queryset = ThreadModel.objects.all()
    serializer_class = ThreadSerializer
class MessageViewset(viewsets.ModelViewSet):
    permission_classes =(AuthorOrRead,)
    queryset = MessageModel.objects.all()
    serializer_class = MessageSerializer
# Create your views here.

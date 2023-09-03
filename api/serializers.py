from rest_framework.serializers import ModelSerializer
from Main1.models import CustomModel,Profile,Post,Comment,MessageModel,ThreadModel

class CustomModelSerializer(ModelSerializer):
    class Meta:
        model = CustomModel
        fields = ['age','gender']

class ProfileSerializer(ModelSerializer):
    class Meta:
        model=Profile
        fields=['name','created','follow']
class PostSerializer(ModelSerializer):
    class Meta:
        model=Post
        fields=['title','body','created_at','updated_now','likes','picture']
class CommentSerializer(ModelSerializer):
    class Meta:
        model=Comment
        fields=['receiver','response',]
class ThreadSerializer(ModelSerializer):
    class Meta:
        model=ThreadModel
        fields=['has_unread','user','receiver']
class MessageSerializer(ModelSerializer):
    class Meta:
        model=MessageModel
        fields=['thread','sender_user','receiver_user','body','image','date','is_read',]
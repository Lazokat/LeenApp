from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomModel,Comment
from django.forms import ModelForm,CharField,Form
class CustomCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomModel
        fields = UserCreationForm.Meta.fields + ('age', 'gender',)

class CustomUserForm(UserChangeForm):
    class Meta:
        model = CustomModel
        fields = UserChangeForm.Meta.fields
class NewComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['receiver',]

class ThreadForm(Form):
  username = CharField(label='', max_length=100)
class MessageForm(Form):
  message = CharField(label='', max_length=1000)
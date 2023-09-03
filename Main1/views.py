from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.views.generic import DetailView,ListView,View
from .forms import CustomCreationForm,NewComment,ThreadForm,MessageForm
from django.db.models import Q
from .models import Profile,Post,Comment,CustomModel,ThreadModel,MessageModel
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
def home(request):
    return render(request,'background.html')

class SignUp(CreateView):
    form_class = CustomCreationForm
    template_name = 'registration/signup.html'
    success_url = '/account/login/'
class Delete(DeleteView):
    model = CustomModel
    template_name = 'Delete_account_form.html'
    success_url = reverse_lazy('leena:all_profile')
def search(request):
    query = request.GET.get("search")
    if query:
        posts = Profile.objects.filter(Q(name__icontains=query))
    else:
        posts = Profile.objects.all().order_by("created")
    return render(request,'Dashboard.html',{'profiles':posts})

def all_profiles(request):
    posts = Profile.objects.all().order_by("-created")
    return render(request, 'Dashboard.html', {'profiles': posts})

class Profile_detail(DetailView):
    model = Profile
    template_name = 'private_profile.html'
    context_object_name = 'private'
    def get_context_data(self, **kwargs):
        query = super().get_context_data(**kwargs)
        model = get_object_or_404(Profile, id=self.kwargs['pk'])
        fol = False
        if model.follow.filter(id=self.request.user.id).exists():
            fol = True
        query['number_follows'] = model.follow.count()
        query['post_followed'] = fol
        return query
class PostCreate(CreateView):
    model = Post
    template_name = 'Post_create.html'
    fields = ['title','body','picture']
    success_url = reverse_lazy('leena:all_post')
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
class PostDetail(DetailView):
    model = Post
    template_name = 'Post_detail.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(
            post_connected=self.get_object()).order_by('-created_at')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewComment(instance=self.request.user)
        model = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if model.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_likes'] = model.likes.count()
        data['post_liked'] = liked
        return data
    def post(self, request, *args, **kwargs):
        new_comment = Comment(receiver=request.POST.get('receiver'),sender=self.request.user,post_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
class PostUpdate(UpdateView):
    model = Post
    fields = ['title','body','picture']
    success_url = reverse_lazy('leena:all_post')
    template_name = 'Post_update.html'
class Post_delete(DeleteView):
    model = Post
    template_name = 'Post_delete_confirm_form.html'
    success_url = reverse_lazy('leena:all_post')
class PostList(ListView):
    model = Post
    template_name = 'Post_list.html'
    context_object_name = 'post'
def post_like(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('leena:post_detail', args=[str(pk)]))
def follow_system(request,pk):
    post=get_object_or_404(Profile,id=request.POST.get('profile_id'))
    if post.follow.filter(id=request.user.id).exists():
        post.follow.remove(request.user)
    else:
        post.follow.add(request.user)
    return HttpResponseRedirect(reverse('leena:my_profile', args=[str(pk)]))
class ProfileCreate(CreateView):
    model = Profile
    fields = ['name','image',]
    template_name = 'profile_create.html'
    success_url = reverse_lazy('leena:all_profile')
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)



class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {
            'form': form
        }
        return render(request, 'create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        try:
            receiver = CustomModel.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                sender_thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                sender_thread.save()
                thread_pk = sender_thread.pk
                return redirect('thread', pk=thread_pk)
        except:
            return redirect('leena:create-thread')
class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if  thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
            message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message'),)
            message.save()
        return redirect('leena:thread', pk=pk)

class ThreadView(View):
  def get(self, request, pk, *args, **kwargs):
    form = MessageForm()
    thread = ThreadModel.objects.get(pk=pk)
    message_list = MessageModel.objects.filter(thread__pk__contains=pk)
    context = {
      'thread': thread,
      'form': form,
      'message_list': message_list
    }
    return render(request, 'thread.html', context)

class ListThreads(View):
  def get(self, request, *args, **kwargs):
      threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
      context = {
        'threads': threads
      }
      return render(request, 'inbox.html', context)

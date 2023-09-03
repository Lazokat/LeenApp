from rest_framework.routers import SimpleRouter
from .views import CustomViewset,PostViewSet,ProfileViewset,CommentViewset,MessageViewset,ThreadViewset
router = SimpleRouter()
router.register("users", CustomViewset, basename="users")
router.register("profile", ProfileViewset, basename="profile")
router.register("comment", CommentViewset, basename="comment")
router.register("post", PostViewSet, basename="post")
router.register("message", MessageViewset, basename="message")
router.register("thread", ThreadViewset, basename="thread")
urlpatterns = router.urls
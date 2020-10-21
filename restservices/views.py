from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers, viewsets, permissions, generics
from django.contrib.auth.models import User
from restservices.serializers import PostSerializer, UserSerializer, TagSerializer, CategorySerializer, CourseSerializer, UserProfileSerializer
from restservices.permissions import IsOwnerOrReadOnly
from page.models import Post, Tag, Category, Course, UserProfile

# Create your views here.
@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'posts' : reverse('post-list',request=request, format=format),
		'tags' : reverse('tag-list',request=request, format=format),
		})

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
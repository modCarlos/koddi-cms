from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from django.conf.urls import url
from models import Ecategory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.authentication import (
    Authentication, ApiKeyAuthentication, BasicAuthentication,
    MultiAuthentication)
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie import fields
from models import EuserProfile, Eevent, Epost, Etag, Ecategory

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'auth/user'
		allowed_methods = ('get','post')
		excludes = ['id', 'email', 'password', 'is_staff', 'is_superuser']
		filtering = {'username': ALL}
		always_return_data = True

		authentication = BasicAuthentication()
		authorization = DjangoAuthorization()

	def authorized_read_list(self, object_list, bundle):
		#if bundle.request.user == bundle.obj:
		return object_list.filter(id=bundle.request.user.id).select_related()

	def apply_authorization_limits(self, request, object_list):
		return object_list.filter(username=request.user.username)

class CreateUserResource(ModelResource):
    #user = fields.ForeignKey('UserResource', 'user', full=True)

    class Meta:
        allowed_methods = ('get')
        always_return_data = True
        #authentication = Authentication()
        #authorization = Authorization()
        #queryset = EuserProfile.objects.all()
        queryset = User.objects.all()
        resource_name = 'auth/register'
        always_return_data = True
        #authentication = ApiKeyAuthentication()

    """
    def hydrate(self, bundle):
        REQUIRED_USER_PROFILE_FIELDS = ("birth_year", "gender", "user")
        for field in REQUIRED_USER_PROFILE_FIELDS:
            if field not in bundle.data:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))

        REQUIRED_USER_FIELDS = ("username", "email", "first_name", "last_name",
                                "raw_password")
        for field in REQUIRED_USER_FIELDS:
            if field not in bundle.data["user"]:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))
        return bundle
    """

    """
    def obj_create(self, bundle, **kwargs):
        try:
            email = bundle.data["email"]
            username = bundle.data["username"]
            if User.objects.filter(email=email):
                raise CustomBadRequest(
                    code="duplicate_exception",
                    message="That email is already used.")
            if User.objects.filter(username=username):
                raise CustomBadRequest(
                    code="duplicate_exception",
                    message="That username is already used.")
        except KeyError as missing_key:
            raise CustomBadRequest(
                code="missing_key",
                message="Must provide {missing_key} when creating a user."
                        .format(missing_key=missing_key))
        except User.DoesNotExist:
            pass

        #self._meta.resource_name = UserProfileResource._meta.resource_name
        return super(CreateUserResource, self).obj_create(bundle, **kwargs)
    """

class UpdateUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/update'
        allowed_methods = ('patch','put')
        excludes = ['id', 'email', 'password', 'is_staff', 'is_superuser']
        filtering = {'username': ALL}
        always_return_data = True

        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id).select_related()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(username=request.user.username)

class EventResource(ModelResource):
    class Meta:
        queryset = Eevent.objects.all()
        resource_name = 'events'
        allowed_methods = ('get')
        excludes = ['id',]
        always_return_data = True

        filtering = {'id': ALL}

        #authentication = ApiKeyAuthentication()

class PostResource(ModelResource):
    event = fields.ForeignKey(EventResource,'event')

    class Meta:
        queryset = Epost.objects.all()
        resource_name = 'posts'
        allowed_methods = ('get')
        excludes = ['id',]
        always_return_data = True

        filtering = { 
            'event' : ALL_WITH_RELATIONS
        }   

        #authentication = ApiKeyAuthentication()
        def get_object_list(self,request):
            return super(PostResource,self).get_object_list(request).filter(event=request.GET['event'])

class CreatePostResource(ModelResource):
    class Meta:
        queryset = Epost.objects.all()
        resource_name = 'post/create'
        allowed_methods = ('post')
        excludes = ['id',]
        always_return_data = True

        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()

class DeletePostResource(ModelResource):
    class Meta:
        queryset = Epost.objects.all()
        resource_name = 'post/delete'
        allowed_methods = ('delete')

        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user=request.user)

class TagResource(ModelResource):
    class Meta:
        queryset = Etag.objects.all()
        resource_name = 'tags'
        allowed_methods = ('get')
        excludes = ['id',]
        always_return_data = True

        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())

class CategoryResource(ModelResource):
    class Meta:
        queryset = Ecategory.objects.all()
        resource_name = 'categories'
        allowed_methods = ('get')
        excludes = ['id',]
        always_return_data = True

        authentication = MultiAuthentication(BasicAuthentication(),ApiKeyAuthentication())
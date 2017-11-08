from django.conf.urls import url

from . import views

urlpatterns = [
	# url(r'^$', views.Index , name='index'),
	# url(r'^posts/(?P<post_id>[0-9]+)/$',views.PostDetail, name='post_detail'),
	# url(r'^category/(?P<category>([\w-])+)/$',views.CategoryIndex, name='category_index'),
	# url(r'^signup/$', views.SignUp, name='signup'),
	# url(r'^profile/(?P<user>([\wd._-])+)/$', views.Profile, name='profile'),
	# url(r'^search/$', views.SearchForum, name='forum_search'),
	# url(r'^messages/(?P<reciever>([\wd._-])+)/$',views.SendShowMsg, name='messages'),
	# url(r'^messages/$',views.MsgIndex, name='msgindex'),
	# url(r'^messager/$',views.MsgIRefresh, name='msgre'),
	# url(r'^messagec/$',views.MsgCount, name='msgco'),
	# url(r'^messages/(?P<reciever>([\wd._-])+)/refresh$',views.MsgRefresh, name='remsg'),
    url(r'^$',views.loginForm,name="loginF")

]

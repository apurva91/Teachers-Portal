from django.conf.urls import url
from django.contrib.auth import views as auth_views
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
    url(r'^login/$', views.loginForm, name="loginF"),
    url(r'^profile/$', views.update_profile, name="profile"),
    url(r'^$', views.dashboard, name="dashboard"),
    url(r'^forgot/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'courses/$', views.list_all_courses, name="list_all_courses"),
]

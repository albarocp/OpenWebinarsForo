from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^foro/$', 'forums.views.forum_view', name='forum_view'),
    url(r'^puntuar_pregunta/(?P<question_id>\d+)/$', 'forums.views.puntuar_pregunta_view', name='puntuar_pregunta_view'),
 	url(r'^quitar_pregunta/(?P<question_id>\d+)/$', 'forums.views.quitar_point_pregunta_view', name='quitar_point_pregunta_view'),
    url(r'^pregunta/(?P<question_id>\d+)/$', 'forums.views.question_and_answer_view', name='question_and_answer_view'),
    url(r'^puntuar_answer/(?P<answer_id>\d+)/$', 'forums.views.vote_answer_view', name='vote_answer_view'),
    url(r'^quitar_answer/(?P<answer_id>\d+)/$', 'forums.views.quit_point_answer', name='quit_point_answer'),
    url(r'^add_answer/(?P<question_id>\d+)/$', 'forums.views.add_answer', name='add_answer'),
    url(r'^add_question/$', 'forums.views.forum_view', name='add_question'),

)

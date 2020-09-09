from django.conf.urls import url

from .views import (
    ImpersonateEndView, ImpersonateStartView, AppsaabazaLoginView, AppsaabazaLogoutView,
    AppsaabazaPasswordChangeDoneView, AppsaabazaPasswordChangeView,
    AppsaabazaPasswordResetCompleteView, AppsaabazaPasswordResetConfirmView,
    AppsaabazaPasswordResetDoneView, AppsaabazaPasswordResetView, UserSetPasswordView
)

urlpatterns_authenticattion = [
    url(regex=r'^login/$', view=AppsaabazaLoginView.as_view(), name='login_view'),
    url(
        regex=r'^logout/$', view=AppsaabazaLogoutView.as_view(), name='logout_view'
    ),
]

urlpatterns_password = [
    url(
        regex=r'^password/change/done/$', name='password_change_done',
        view=AppsaabazaPasswordChangeDoneView.as_view()
    ),
    url(
        regex=r'^password/change/$', name='password_change_view',
        view=AppsaabazaPasswordChangeView.as_view()
    ),
    url(
        regex=r'^password/reset/complete/$',
        name='password_reset_complete_view',
        view=AppsaabazaPasswordResetCompleteView.as_view()
    ),
    url(
        regex=r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        name='password_reset_confirm_view',
        view=AppsaabazaPasswordResetConfirmView.as_view()
    ),
    url(
        regex=r'^password/reset/done/$',
        name='password_reset_done_view',
        view=AppsaabazaPasswordResetDoneView.as_view()
    ),
    url(
        regex=r'^password/reset/$', name='password_reset_view',
        view=AppsaabazaPasswordResetView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/set_password/$',
        name='user_set_password', view=UserSetPasswordView.as_view()
    ),
    url(
        regex=r'^users/multiple/set_password/$',
        name='user_multiple_set_password', view=UserSetPasswordView.as_view()
    )
]

urlpatterns_user_impersonation = [
    url(
        regex=r'^impersonate/end/$', name='impersonate_end',
        view=ImpersonateEndView.as_view()
    ),
    url(
        regex=r'^impersonate/start/$', name='impersonate_start',
        view=ImpersonateStartView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_authenticattion)
urlpatterns.extend(urlpatterns_password)
urlpatterns.extend(urlpatterns_user_impersonation)

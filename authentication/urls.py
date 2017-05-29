from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'authentication'

urlpatterns=[
	url(r'^sign-up/', views.SignUpView.as_view(), name='sign_up'),
	url(r'^sign-in/', views.SignInView.as_view(), name='sign_in'),
	url(r'^logout/', views.LogoutView.as_view(), name='logout'),
	url(r'^edit-profile/(?P<pk>\d+)/', views.EditProfileView.as_view(), name='edit_profile'),
	url(r'^show-profile/', views.UserProfileView.as_view(), name='show_profile'),
	url(r'^change-password/', views.ChangePasswordView.as_view(), name='change_password'),
	url(r'^delete-account/(?P<pk>\d+)/', views.DeleteUserAccountView.as_view(), name='delete_account'),
	url(r'^setting/', views.SettingView.as_view(), name='setting'),
	
]	

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.home, name='home'),

	path('signup/', views.signup, name='signup'),
	path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user='profile'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

	path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
	path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
	path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
	path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

	path('profile/', views.ProfileView.as_view(), name='profile'),
	path('profile/polls/', views.ProfilePollsView.as_view(), name='profilepolls'),
	path('profile/polls/<int:pk>/', views.PollsDetailView.as_view(), name='pollsdetail'),
	path('profile/polls/<int:pk>/result/', views.PollsResultView.as_view(), name='pollsresult'),

	path('profile/mypolls/', views.ProfileMyPollsView.as_view(), name='profilemypolls'),
	path('profile/createpoll/', views.profilecreatepoll, name='profilecreatepoll'),
	path('profile/user/<str:username>/', views.UserProfilePollsView.as_view(), name='userprofilepolls'),

	path('profile/update/', views.profileupdate, name='profileupdate'),
]
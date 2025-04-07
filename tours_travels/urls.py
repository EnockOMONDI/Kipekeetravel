
from django.contrib import admin
from django.urls import path,include
from . import views as tours_travels_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static







urlpatterns = [

    path('jet/', include('jet.urls', 'jet')), 
    path('admin/', admin.site.urls),
    #path('',tours_travels_views.home,name = 'home'),
    path('', include(('dede.urls', 'dede'), namespace='dede')),
    path('old/', include(('users.urls', 'users'), namespace='home')),
    path('tours/', include(('adminside.urls', 'adminside'), namespace='adminside')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/index.html'),name='logout'),
    path('mail/',tours_travels_views.mail,name='mail'),
  
    

]


if settings.DEBUG == True:
    # static function below returns a list of url patterns of static path
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)  




    
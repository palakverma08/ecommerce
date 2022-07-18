from django.urls import path 
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('',views.home ,name="home" ),

    path('register/',views.registerPage ,name="register"),
    path('login/',views.loginPage ,name="login"),
    path('logout/',views.logoutUser ,name="logout"),

    path('account/',views.accountSettings,name="account"),

     path('product/',views.product ,name="product"),
      path('main/',views.main),
     path('navbar/',views.navbar),
      path('customer/<str:pk_test>/',views.customer,name="customer" ),
     
      path('user',views.userPage ,name="user-page"),
     path('create_order/<str:pk>/',views.createOrder,name="create_order"),
      path('update_order/<str:pk>/',views.updateOrder,name="update_order"),
     # path('delete_order/<str:pk>/',views.deleteOrder,name="delete_order"),
     path('delete_order/<str:pk>/',views.deleteOrder,name="delete_order"),
]
#urlpatterns += staticfiles_urlpatterns()
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
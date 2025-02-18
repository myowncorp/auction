from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name='create_listing'),
    path("listing/<int:listing_id>", views.listing, name='listing'),
    path("<str:user>/watchlist", views.watch_list, name='watch_list'),
    path('categories', views.categories, name='categories'),
    path('category/<str:category>', views.category, name='category')
]

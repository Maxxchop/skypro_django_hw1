from django.urls import path

from ads import views

urlpatterns = [
    path("", views.CatListView.as_view()),
    path("<int:pk>/", views.CatDetailView.as_view()),
    path("create/", views.CatCreateView.as_view()),
    path("<int:pk>/update/", views.CatUpdateView.as_view()),
    path("<int:pk>/delete/", views.CatDeleteView.as_view()),
]
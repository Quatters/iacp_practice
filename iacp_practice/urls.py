from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from app import views
from iacp_practice import settings

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),

    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),

    path('news_archive/', views.NewsArchiveListView.as_view(), name='news_archive_list'),
    path('news_archive/<int:pk>', views.NewsArchiveDetailView.as_view(), name='news_archive_detail'),

    path('staff/', views.StaffListView.as_view(), name='publisher_list'),
    path('staff/<int:pk>', views.StaffDetailView.as_view(), name='publisher_detail'),

    path('publications/', views.PublicationListView.as_view(), name='publication_list'),
    path('publications/<int:pk>', views.PublicationDetailView.as_view(), name='publication_detail'),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


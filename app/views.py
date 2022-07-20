from django.db.models import Subquery
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from app import models

DEFAULT_PAGE_ITEMS_COUNT = 10


class HomeView(ListView):
    queryset = models.NewsItem.objects.only(
        'id',
        'name',
        'thumbnail',
    ).order_by('-id')[:5]
    template_name = 'app/index.html'


class NewsListView(ListView):
    queryset = models.NewsItem.objects.only('id', 'name', 'thumbnail', 'tags')
    paginate_by = DEFAULT_PAGE_ITEMS_COUNT
    template_name = 'app/news/list.html'


class NewsDetailView(DetailView):
    model = models.NewsItem
    template_name = 'app/news/detail.html'


class PublisherListView(ListView):
    queryset = models.Publisher.objects.only(
        'id',
        'user__first_name',
        'user__last_name',
        'patr',
        'photo',
    )
    paginate_by = DEFAULT_PAGE_ITEMS_COUNT
    template_name = 'app/staff/list.html'


class PublisherDetailView(DetailView):
    model = models.Publisher
    template_name = 'app/staff/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.publications = models.Publication.objects.filter(authors__user=obj.user)
        return obj


class PublicationListView(ListView):
    queryset = models.Publication.objects.only(
        'name',
        'authors',
        'publication_date'
    )
    template_name = 'app/publications/list.html'
    paginate_by = DEFAULT_PAGE_ITEMS_COUNT


class PublicationDetailView(DetailView):
    model = models.Publication
    template_name = 'app/publications/detail.html'

from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from app.models import Article


def index(request):
    return render(request, 'app/index.html')


class NewsListView(ListView):
    queryset = Article.objects.only('id', 'name', 'thumbnail')
    paginate_by = 5
    template_name = 'app/news/list.html'


class NewsDetailView(DetailView):
    model = Article
    template_name = 'app/news/detail.html'

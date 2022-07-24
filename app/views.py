from django.views.generic import ListView, DetailView

from app import models

DEFAULT_PAGE_ITEMS_COUNT = 10


class HomeView(ListView):
    queryset = models.NewsItem.objects.only(
        'id',
        'name',
        'thumbnail',
    ).filter(is_public=True, is_archived=False)[:5]
    template_name = 'app/index.html'


class NewsListView(ListView):
    queryset = models.NewsItem.objects.filter(
        is_public=True,
        is_archived=False
    ).only('id', 'name', 'thumbnail', 'tags')
    paginate_by = DEFAULT_PAGE_ITEMS_COUNT
    template_name = 'app/news/list.html'

    def get_queryset(self):
        if tag := self.request.GET.get('tag'):
            self.queryset = self.queryset.filter(tags__name=tag)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = models.Tag.objects.all()
        if current_tag := self.request.GET.get('tag'):
            context['current_tag'] = current_tag
        return context


class NewsDetailView(DetailView):
    queryset = models.NewsItem.objects.filter(is_public=True, is_archived=False)
    template_name = 'app/news/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_path'] = '/news/'
        return context


class NewsArchiveListView(NewsListView):
    queryset = models.NewsItem.objects.filter(
        is_public=True,
        is_archived=True
    ).only('id', 'name', 'thumbnail', 'tags')


class NewsArchiveDetailView(NewsDetailView):
    queryset = models.NewsItem.objects.filter(is_public=True, is_archived=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_path'] = '/news_archive/'
        return context


class StaffListView(ListView):
    queryset = models.Staff.objects.only(
        'id',
        'user__first_name',
        'user__last_name',
        'patr',
        'photo',
    )
    paginate_by = DEFAULT_PAGE_ITEMS_COUNT
    template_name = 'app/staff/list.html'


class StaffDetailView(DetailView):
    model = models.Staff
    template_name = 'app/staff/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.publications = models.Publication.objects.filter(staff_authors__user=obj.user)
        return obj


class PublicationListView(ListView):
    queryset = models.Publication.objects.only('name', 'staff_authors', 'other_authors', 'year')
    template_name = 'app/publications/list.html'
    paginate_by = DEFAULT_PAGE_ITEMS_COUNT

    def get_queryset(self):
        if year := self.request.GET.get('year'):
            self.queryset = self.queryset.filter(year=year)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = models.Publication.objects.values_list('year', flat=True).distinct().order_by('-year')
        current_year = self.request.GET.get('year', '')
        if current_year.isdigit():
            context['current_year'] = int(current_year)
        return context


class PublicationDetailView(DetailView):
    model = models.Publication
    template_name = 'app/publications/detail.html'

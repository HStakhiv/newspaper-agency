from django.shortcuts import render
from django.views import generic

from newsapp.models import Redactor, Topic, Newspaper


def index(request):
    num_redactors = Redactor.objects.count()
    num_topics = Topic.objects.count()
    num_newspapers = Newspaper.objects.count()

    context = {
        "num_redactors": num_redactors,
        "num_topics": num_topics,
        "num_newspapers": num_newspapers,
    }

    return render(request, "newsapp/index.html", context=context)


class TopicListView(generic.ListView):
    model = Topic
    queryset = Topic.objects.order_by("name")
    paginate_by = 5


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 5
    queryset = Newspaper.objects.select_related("topic")


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 5

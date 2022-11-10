from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from newsapp.form import (
    NewspaperForm,
    RedactorCreationForm,
    RedactorYearsUpdateForm,
)
from newsapp.models import Redactor, Topic, Newspaper


@login_required
def index(request):
    num_redactors = Redactor.objects.count()
    num_topics = Topic.objects.count()
    num_newspapers = Newspaper.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_topics": num_topics,
        "num_newspapers": num_newspapers,
        "num_visits": num_visits + 1,
    }

    return render(request, "newsapp/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    queryset = Topic.objects.order_by("name")
    paginate_by = 5


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newsapp:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newsapp:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("newsapp:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 5
    queryset = Newspaper.objects.select_related("topic")


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newsapp:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newsapp:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newsapp:newspaper-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspaper__topic")


class RedactorCreationView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorYearsUpdateForm


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("newsapp:redactor-list")


@login_required
def toggle_assign_to_newspaper(request, pk):
    redactor = Redactor.objects.get(id=request.user.id)
    if Newspaper.objects.get(id=pk) in redactor.newspaper.all():
        redactor.newspaper.remove(pk)
    else:
        redactor.newspaper.add(pk)
    return HttpResponseRedirect(
        reverse_lazy("newsapp:newspaper-detail", args=[pk])
    )

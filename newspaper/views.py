from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from newspaper.form import (
    NewspaperForm,
    RedactorCreationForm,
    RedactorYearsUpdateForm,
    TopicSearchForm,
    RedactorSearchForm,
    NewspaperSearchForm,
)
from newspaper.models import Redactor, Topic, Newspaper


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

    return render(request, "newspaper/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 5
    queryset = Topic.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data()

        name = self.request.GET.get("name", "")

        context["search_form"] = TopicSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        form = TopicSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("newspaper:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 5
    queryset = Newspaper.objects.select_related("topic")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data()

        title = self.request.GET.get("title", "")

        context["search_form"] = NewspaperSearchForm(
            initial={"title": title}
        )

        return context

    def get_queryset(self):
        form = NewspaperSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )

        return self.queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newspaper:newspaper-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5
    queryset = Redactor.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )

        return context

    def get_queryset(self):
        form = RedactorSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return self.queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspaper__topic")


class RedactorCreationView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("newspaper:redactor-list")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorYearsUpdateForm


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("newspaper:redactor-list")


@login_required
def toggle_assign_to_newspaper(request, pk):
    redactor = Redactor.objects.get(id=request.user.id)
    if Newspaper.objects.get(id=pk) in redactor.newspaper.all():
        redactor.newspaper.remove(pk)
    else:
        redactor.newspaper.add(pk)
    return HttpResponseRedirect(
        reverse_lazy("newspaper:newspaper-detail", args=[pk])
    )

from django.http import HttpRequest, HttpResponse
from django.views import generic
from .models import Question


class IndexView(generic.ListView):

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):

        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request: HttpRequest, question_id):

    return HttpResponse(f'You are voting for question {question_id}')

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Question



def index(request: HttpRequest):

    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    context = {
        'latest_question_list': latest_question_list,
    }

    return render(request, 'polls/index.html', context)


def details(request: HttpRequest, question_id):

    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/detail.html', {'question': question})


def results(request: HttpRequest, question_id):

    response = f'You are looking at the results of question: '

    return HttpResponse(f'{response} {question_id}')


def vote(request: HttpRequest, question_id):

    return HttpResponse(f'You are voting for question {question_id}')

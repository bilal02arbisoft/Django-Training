from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Question, Choice
from django.urls import reverse
from .forms import ContactForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def custom_404(request, exception):

    return render(request, 'polls/404.html', status=404)


def home(request):

    if request.user.is_authenticated:

        return HttpResponseRedirect(reverse('polls:index'))

    return render(request, 'polls/home.html')


class IndexView(LoginRequiredMixin, generic.ListView):

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):

        return Question.objects.order_by("-pub_date")[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):

    model = Question
    template_name = 'polls/detail.html'


class ResultsView(LoginRequiredMixin, generic.DetailView):

    model = Question
    template_name = 'polls/results.html'


class ContactView(LoginRequiredMixin, View):

    template_name = 'polls/contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = []
            if cc_myself:
                recipients.append(sender)

            return HttpResponseRedirect(reverse('polls:thanks'))

        return render(request, self.template_name, {'form': form})


@login_required()
def thanks(request):

    return HttpResponse('Your Contact Form Submitted Successfully')


@login_required()
def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {
                'question': question,
                'error_message': "You didn't select a choice.",
            },
        )

    else:

        selected_choice.votes = F('votes') + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def login_view(request):

    return render(request, 'registration/login.html')

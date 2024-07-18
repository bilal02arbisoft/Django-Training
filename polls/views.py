from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Question, Choice
from django.urls import reverse
from .forms import ContactForm
from django.core.mail import send_mail


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


def contact_view(request):

    if request.method == "POST":

        form = ContactForm(request.POST)
        if form.is_valid():

            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = []
            if cc_myself:

                recipients.append(sender)

            # send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect(reverse('polls:thanks'))
    else:

        form = ContactForm()

    return render(request, 'polls/contact.html', {'form': form})


def thanks(request):

    return HttpResponse('Your Contact Form Submitted Successfully')


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

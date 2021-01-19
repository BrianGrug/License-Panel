from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from polls.models import Question


class IndexView(ListView):
    template_name = 'index.html'
    question_list = Question.objects.all()

    def At_least_one_question(self):
        return Question.objects.get_queryset().exists()

    def get_queryset(self):
        filtered_question = Question.objects.all()[:5]
        return filtered_question


class ResultView(DetailView):
    model = Question
    template_name = 'result.html'
    test = None


class DetailView(DetailView):
    model = Question
    template_name = 'detail.html'


def vote(request, question_id):
    my_question = get_object_or_404(Question, pk=question_id)
    try:
        my_reponse = my_question.reponse_set.get(pk=request.POST['reponse'])
    except (my_reponse.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': my_question})
    else:
        my_reponse.nb_vote += 1
        my_reponse.save()
    return HttpResponseRedirect(reverse('result', args='question_id'))

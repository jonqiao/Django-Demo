from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


# Create your views here.
def fbv_index(request):
  # get_list_or_404() -> Question.objects.filter()
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  context = {'latest_question_list': latest_question_list}
  return render(request, 'polls/fbvIndex.html', context)


class IndexView(generic.ListView):
  template_name = 'polls/cbvIndex.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    """Return the last five published questions."""
    return Question.objects.order_by('-pub_date')[:5]


def fbv_detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/fbvDetail.html', {'question': question})


class DetailView(generic.DetailView):
  model = Question
  template_name = 'polls/cbvDetail.html'


def fbv_results(request, question_id):
  # get_object_or_404() -> Question.objects.get()
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/fbvResults.html', {'question': question})


class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/cbvResults.html'


def fbv_vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/fbvDetail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:fbvResults', args=(question.id,)))


def cbv_vote(request, pk):
  question = get_object_or_404(Question, pk=pk)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/cbvDetail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:cbvResults', args=(question.id,)))

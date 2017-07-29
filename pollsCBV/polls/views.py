from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from polls.models import Question, Choice


class PollsIndexView(ListView):
    # model = Question
    queryset = Question.objects.order_by('-pub_date')[:5]
    template_name = 'polls/index.html'


class PollsDetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'


class PollsResultView(DetailView):
    model = Question
    template_name = 'polls/result.html'


def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        select = request.POST['choice']
        selected_choice = question.choice_set.get(pk=select)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:result', question.id)


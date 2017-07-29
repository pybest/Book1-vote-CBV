from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from polls.models import Question, Choice
# from polls_new.forms import PollsRadioForm
from polls_new.forms import QuestionRadioForm


class PollsIndexView(ListView):
    # model = Question
    queryset = Question.objects.order_by('-pub_date')[:5]
    template_name = 'polls_new/index.html'


class PollsDetailView(DetailView):
    model = Question
    template_name = 'polls_new/detail.html'


class PollsResultView(DetailView):
    model = Question
    template_name = 'polls_new/result.html'


# def vote(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     try:
#         select = request.POST['choice']
#         selected_choice = question.choice_set.get(pk=select)
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls_new/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         return redirect('polls_new:result', question.id)


class PollsFormView(FormView):
    # form_class = PollsRadioForm
    form_class = QuestionRadioForm
    template_name = 'polls_new/detail.html'
    # success_url = reverse_lazy('polls_new:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        object = Question.objects.first()
        kwargs.update({'question': object})
        return kwargs

    def form_valid(self, form):
        object = Question.objects.first()
        select = form.cleaned_data['my_choice_field']
        selected_choice = object.choice_set.get(pk=select)

        selected_choice.votes += 1
        selected_choice.save()
        # return redirect('polls_new:result', object.id)
        return super().form_valid(form)

    def get_success_url(self):
        object = Question.objects.first()
        return reverse_lazy('polls_new:result', kwargs={'pk': object.id})


class PollsSOMFV(SingleObjectMixin, FormView):
    model = Question
    form_class = QuestionRadioForm
    template_name = 'polls_new/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # object = Question.objects.first()
        kwargs.update({'question': self.object})
        return kwargs

    def form_valid(self, form):
        # object = Question.objects.first()
        select = form.cleaned_data['my_choice_field']
        selected_choice = self.object.choice_set.get(pk=select)

        selected_choice.votes += 1
        selected_choice.save()
        # return redirect('polls_new:result', object.id)
        return super().form_valid(form)

    def get_success_url(self):
        # object = Question.objects.first()
        return reverse_lazy('polls_new:result', kwargs={'pk': self.object.id})

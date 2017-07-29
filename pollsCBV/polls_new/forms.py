from django import forms

from polls.models import Question


def get_choices():
    # choiceList = [
    #     (1, 'aaa'),
    #     (2, 'bbb'),
    #     (3, 'CCC'),
    # ]

    object = Question.objects.first()
    choiceList = [(i.pk, i.choice_text) for i in object.choice_set.all()]
    return choiceList


'''
class PollsRadioForm(forms.Form):

    # choiceList = [
    #     (1, 'aaa'),
    #     (2, 'bbb'),
    #     (3, 'ccc'),
    # ]

    question = Question.objects.first()
    my_choice_field = forms.ChoiceField(
        # label="What's your name ?",
        label=question.question_text,
        choices=get_choices(),
        widget=forms.RadioSelect,
    )
'''


class QuestionRadioForm(forms.Form):

    # question = Question.objects.first()
    # my_choice_field = forms.ChoiceField(
    #     # label="What's your name ?",
    #     label=question.question_text,
    #     choices=get_choices(),
    #     widget=forms.RadioSelect,
    # )

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['my_choice_field'] = forms.ChoiceField(
            label=question.question_text,
            # choices=get_choices(),
            choices=self.get_choices(question),
            widget=forms.RadioSelect,
        )

    def get_choices(self, question):
        # object = Question.objects.first()
        choiceList = [(i.pk, i.choice_text) for i in question.choice_set.all()]
        return choiceList
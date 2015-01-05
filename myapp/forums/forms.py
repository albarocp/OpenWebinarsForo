from django.forms import ModelForm
from .models import Answer, Question


class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ['title', 'answer']


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		exclude = ['user']
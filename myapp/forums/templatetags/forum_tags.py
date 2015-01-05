from django import template
from django.contrib.auth.models import User
from ..forms import QuestionForm




from forums.models import Question, Answer, Point


register = template.Library()

#@register.simple_tag
@register.filter
def is_user_scored(question, user):
	return question.have_user_scored(user)


@register.filter
def is_user_scored_answer(answer, user):
	return answer.user_voted_answer(user)


@register.inclusion_tag('foro.html')
def get_form_question():
	forms = QuestionForm()
	return {"forms":forms,}

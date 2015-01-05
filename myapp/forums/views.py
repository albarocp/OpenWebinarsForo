import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext


from .models import Question, Answer, Point
from .forms import AnswerForm, QuestionForm

"""
Vista Principal foro
"""

def forum_view(request):

	if request.method == 'POST':
		form = QuestionForm(request.POST)

		if form.is_valid():
			question = form.save(commit=False)
			question.user = request.user
			question.save()


			#back = request.META.get('HTTP_REFERER', None)
			response_data = {'form_saved':True,}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
			#return redirect('/foro/')
		else:
			response_data = {'form_saved': False, 'errors': form.errors}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		form = QuestionForm()

	args = {}
	args['questions'] = Question.objects.all()
	args['form'] = form
	return render(request, 'foro.html', args)

"""
Puntua una pregunta
"""
def puntuar_pregunta_view(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	
	if not question.have_user_scored(request.user):
		Point.objects.create(question=question, user=request.user)

	back = request.META.get('HTTP_REFERER', None)
	return HttpResponseRedirect(back)


"""
Quita el punto dado por el usuario a una pregunta
"""
def quitar_point_pregunta_view(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	if question.have_user_scored(request.user):
		remove_question=Point.objects.get(question=question, user=request.user)
		remove_question.delete()

	back = request.META.get('HTTP_REFERER', None)
	return HttpResponseRedirect(back)


"""
Detalla una pregunta con sus respectivo respuesta
"""
def question_and_answer_view(request, question_id):
	if request.POST:
		form = AnswerForm(request.POST)

		if form.is_valid():
			answer = form.save(commit=False)
			answer.user = request.user
			answer.question = Question.objects.get(pk=question_id)
			answer.save()

			response_data = {'form_saved':True,}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			response_data = {'form_saved': False, 'errors': form.errors}
			return HttpResponse(json.dumps(response_data), content_type="application/json")			
	else:
		form = AnswerForm()

	args = {}
	args['question'] = get_object_or_404(Question, pk=question_id)
	args['answers'] = Answer.objects.filter(question=args['question'])
	args['form'] = form
	
	return render(request, 'detailed.html', args)


"""
Asigna un punto a una repuesta
"""
def vote_answer_view(request, answer_id):
	answer = get_object_or_404(Answer, pk=answer_id)

	if not answer.user_voted_answer(request.user):
		Point.objects.create(answer=answer, user=request.user)

	back = request.META.get('HTTP_REFERER', None)
	return HttpResponseRedirect(back)


"""
Quita el punto dado por el usuario a una respuesta
"""
def quit_point_answer(request, answer_id):
	answer = get_object_or_404(Answer, pk=answer_id)

	if answer.user_voted_answer(request.user):
		remove_answer = Point.objects.get(answer=answer, user=request.user)
		remove_answer.delete()

	back = request.META.get('HTTP_REFERER', None)
	return HttpResponseRedirect(back)


def add_answer(request, question_id):
	if request.POST:
		form = AnswerForm(request.POST)

		if form.is_valid():
			answer = form.save(commit=False)
			answer.user = request.user
			answer.question = Question.objects.get(pk=question_id)
			answer.save()

			#back = request.META.get('HTTP_REFERER', None)
			return redirect('/pregunta/'+question_id+'/')
	else:
		form = AnswerForm()

	return render(request, 'add_answer.html', {'form': form})
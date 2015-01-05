from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Question(models.Model):
	title = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	question = models.TextField()
	user = models.ForeignKey(User)

	def __str__(self):
		return self.question

	def __unicode__(self):
		return self.question

	def get_points(self):
		points = Point.objects.filter(question=self).count()
		return points

	def have_user_scored(self, us):
		voted = False
		if Point.objects.filter(user=us, question=self).count() > 0:
			voted = True

		return voted

	def get_num_answer(self):
		num_answer = Answer.objects.filter(question=self).count()
		
		return num_answer

class Answer(models.Model):
	title = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	answer = models.TextField()
	question = models.ForeignKey(Question)
	user = models.ForeignKey(User)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_point_answer(self):
		point = Point.objects.filter(answer=self).count()
		return point

	def user_voted_answer(self, user):
		voted = False
		if Point.objects.filter(answer=self, user=user).count() > 0:
			voted = True

		return voted


class Point(models.Model):
	pub_date = models.DateTimeField('date point', auto_now_add = True)
	question = models.ForeignKey(Question, blank=True, null=True)
	answer = models.ForeignKey(Answer , blank=True, null=True)
	user = models.ForeignKey(User)

	def __str__(self):
		if self.answer != None:
			return '%s - %s ' % (self.user, self.answer.answer)
		else:
			return '%s - %s ' % (self.user, self.question.question)


	def __unicode__(self):
		if self.answer != None:
			return u'%s - %s ' % (self.user, self.answer.answer)
		else:
			return u'%s - %s ' % (self.user, self.question.question)


	def clean(self):

		if self.id is None: #  (actualmente no existe el registro ) Compruena si se esta creando un nuevo registro
			# Inicializamos point_add_answer y posint_add_question a 0
			point_add_answer = point_add_question = 0

			# Si self.answer no es None consul =tamos al modelo
			if self.answer != None:
				point_add_answer = Point.objects.filter(user=self.user, answer=self.answer).count()

			# Si self.question no es None consultamos al modelo
			if self.question != None:
				point_add_question = Point.objects.filter(user=self.user, question=self.question).count()

			if point_add_answer > 0 or point_add_question > 0:
				raise ValidationError("You can not score")

	
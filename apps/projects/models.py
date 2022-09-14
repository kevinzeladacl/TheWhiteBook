from django.db import models
from apps.users.models import User
from django_quill.fields import QuillField


class Project(models.Model): 
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name


class Chapter(models.Model): 
	project = models.ForeignKey(Project,on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	body = QuillField()


	def __str__(self):
		return self.name

class Character(models.Model): 
	project = models.ForeignKey(Project,on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	is_global = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Place(models.Model): 
	project = models.ForeignKey(Project,on_delete=models.CASCADE)
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Resource(models.Model): 
	project = models.ForeignKey(Project,on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	is_global = models.BooleanField(default=False)

	def __str__(self):
		return self.name
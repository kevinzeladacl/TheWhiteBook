from django.db import models
from apps.users.models import User
from django_quill.fields import QuillField


class Project(models.Model): 
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=250,blank=True)
	resume = models.CharField(max_length=1000,blank=True)
	

	def __str__(self):
		return self.name


class Chapter(models.Model): 
	project = models.ForeignKey(Project,on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=250,blank=True)
	list_status = (
		(0,'Borrador'),
		(1,'Progreso'),
		(2,'Terminado'),
		(3,'Descartado'),
	)
	status = models.IntegerField(default=0,choices=list_status)
	body = QuillField()
	


	def __str__(self):
		return self.name

class NotesChapter(models.Model): 
	chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
	body = models.CharField(max_length=30)

	def __str__(self):
		return self.body


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
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import post_save

from django_facebook.models import FacebookProfileModel
from django_facebook import signals


PASSION_CHOICES = (

	('Art','Art'),
	('Sports','Sports'),
	('Science', 'Science'),
	('Technology','Technology'),

	)


def make_upload_path(instance, filename):
    file_root, file_ext = os.path.splitext(filename)
    dir_name = '{module}/{model}'.format(module=instance._meta.app_label, model=instance._meta.module_name)
    file_root = unicode(uuid.uuid4())
    name = os.path.join(settings.MEDIA_ROOT, 'images' ,dir_name, file_root + file_ext.lower())
    # Delete existing file to overwrite it later
    if instance.pk:
        while os.path.exists(name):
            os.remove(name)

    return os.path.join(dir_name, file_root + file_ext.lower())


class Picture(models.Model):
    picture = models.ImageField(upload_to=make_upload_path, blank=True)
    owner = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.picture.url

    def get_url(self):
        return str(self.picture.url).split("?")[0]


class Passion(models.Model):
	owner = models.ForeignKey(User, related_name='owner by passion')
	category = models.CharField(max_length=40, choices=PASSION_CHOICES)
	name = models.CharField(max_length=40)
	video_url = models.URLField(max_length=100)
	pictures = models.ManyToManyField(Picture, blank=True, null=True)
	disciples = models.ManyToManyField(User, blank=True, related_name='passion disciples')
	description = models.CharField(max_length=1000)
	location = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % (self.name)

	def get_youtube_id(self):
		return self.video_url.split("v=")[1]


class Profile(FacebookProfileModel):
	user = models.OneToOneField(User, related_name='profile user')
	picture = models.ImageField(upload_to=make_upload_path)#default = '/media/img/cuantoo_profile_picture.png')
	location = models.CharField(max_length=100)
	bio = models.CharField(max_length=500)
	disciples = models.ManyToManyField(User, blank=True, related_name='profile disciples')
	counselors = models.ManyToManyField(User, blank=True, related_name='profile counselors')
	teach_passions = models.ManyToManyField(Passion)

	def __unicode__(self):
		return u'%s' % (self.user)

	#Create profile when new user
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	#Signal to create user profile
	post_save.connect(create_user_profile, sender=User)


class Meeting(models.Model):
	passion = models.ForeignKey(Passion)
	counselor = models.ForeignKey(User, related_name='meeting counselor')
	disciples = models.ManyToManyField(User, related_name='meeting disciples', blank=True, null=True)
	details = models.CharField(max_length=1024)
	date = models.DateTimeField()
	is_presential = models.BooleanField()

	def __unicode__(self):
		return u'%s' % self.passion




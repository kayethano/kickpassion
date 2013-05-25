#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django_facebook.models import FacebookProfileModel
from django_facebook import signals

from django.http import HttpResponse

from kickpassion.engine.thumbs import ImageWithThumbsField

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

class Profile(FacebookProfileModel):
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to=make_upload_path)#default = '/media/img/cuantoo_profile_picture.png')
	name = models.CharField(max_length=40)
	location = models.CharField(max_length=100)
	bio = models.CharField(max_length=500)
	disciples = models.ManyToManyField(User, blank=True)
	counselors = models.ManyToManyField(User, blank=True)

	def __unicode__(self):
		return u'%s' % (self.user)

	#Create profile when new user
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	#Create new student info by user
	#def facebook_register(sender,facebook_data, **kwargs):
	#	student = Student.objects.create(name=facebook_data['facebook_name'], facebook=facebook_data['facebook_profile_url'])

	#Signal to create user profile
	post_save.connect(create_user_profile, sender=User)
	signals.facebook_user_registered.connect(facebook_register, sender=User)

class Passion(models.Model):
	name = models.CharField(max_length=20)
	video_url = models.CharField(max_length=40)
	pictures = models.ManyToManyField(Picture)
	description = models.CharField(max_length=1000)
	location = models.CharField(max_length=100)
	counselors = models.ManyToManyField(User, blank=True)

	def __unicode__(self):
		return u'%s' % (self.name)
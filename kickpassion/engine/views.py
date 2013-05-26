from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.utils import simplejson

from kickpassion.engine.models import Passion, Picture, Meeting, Profile
from kickpassion.engine.forms import PassionForm, MeetingForm, ProfileForm


@login_required(login_url='/login/')
def passion(request):
	if request.method == 'POST':
		form = PassionForm(request.POST, request.FILES)
		if form.is_valid():
			pictures = []

			category = form.cleaned_data['category']
			name = form.cleaned_data['name']
			video_url = form.cleaned_data['video_url']
			description = form.cleaned_data['description']
			location = form.cleaned_data['location']

			#Verifica cada campo de tipo input file, si el usuario lo uso, entonces lo agrega al diccionario para enseguida guardarlos
			pictures.append(form.cleaned_data['picture1'])
			if form.cleaned_data['picture2'] is not None:
				pictures.append(form.cleaned_data['picture2'])
			if form.cleaned_data['picture3'] is not None:
				pictures.append(form.cleaned_data['picture3'])
			if form.cleaned_data['picture4'] is not None:
				pictures.append(form.cleaned_data['picture4'])
			if form.cleaned_data['picture5'] is not None:
				pictures.append(form.cleaned_data['picture5'])

			passion = Passion.objects.create(
				owner = request.user,
				category = category,
				name = name,
				video_url = video_url,
				description = description,
				location = location
				)

			for picture in pictures:
				thisPicture = Picture(owner = request.user, picture = picture)
				thisPicture.save()
				passion.pictures.add(thisPicture)
				passion.save()

			return HttpResponseRedirect('/passion/%s' % passion.pk )
	else:
		form = PassionForm()
	return render_to_response('passion.html', 
		{'form':form}, context_instance=RequestContext(request))

def view_passion(request, passionID):
	passion = get_object_or_404(Passion, pk=passionID)
	return render_to_response('view_passion.html',
		{'passion':passion}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def join_passion(request,passionID,userID):
	passion = get_object_or_404(Passion, pk=passionID)
	user = get_object_or_404(User, pk=userID)
	#Add user to passion
	passion.disciples.add(user)
	passion.save()
	#Add passion to user
	user.get_profile().passions.add(passion)
	user.save()

	return HttpResponse('JOIN OK')


@login_required(login_url='/login/')
def create_meeting(request, passionID):
	#Validate counselor is owner of meeting
	passion = get_object_or_404(Passion, owner=request.user)
	if request.method == 'POST':
		form = MeetingForm(request.POST)
		if form.is_valid():
			meeting = form.save(commit=False)
			meeting.passion = passion
			meeting.counselor = request.user
			return HttpResponseRedirect('/')
	else:
		form = MeetingForm()
	return render_to_response('meeting.html',
		{'form':form}, context_instance=RequestContext(request))


def view_meeting(request, meetingID):
	meeting = get_object_or_404(Meeting, pk = meetingID)
	return render_to_response('view_meeting.html', 
		{'meeting':meeting}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def join_meeting(request,meetingID):
	meeting = get_object_or_404(Meeting, pk=meetingID)
	meeting.disciples.add(request.user)
	meeting.save()
	return HttpResponse('JOIN MEETING OK')

def view_profile(request, profileName):
	#dic={}
	#lst=[]
	#x=1
	for p in Profile.objects.all():
		if profileName == p.user.username:
			return render_to_response('view_profile.html',
				{'person':p}, context_instance=RequestContext(request))
		#dic.update({'%s' % (x):u.user.username})
		#lst.append(p.user.username)
		#x=x+1
	return HttpResponse('Sin Resultados') 
	#ob = get_object_or_404(Profile, pk=3)
	#dic.update({'1':ob.user.username})

@login_required(login_url='/login/')
def edit_profile(request, profileName):
	valid=0
	for p in Profile.objects.all():
		if profileName == p.user.username:
			valid=1
	if valid==1:
	    if request.method == 'POST':
	        form = ProfileForm(request.POST, instance = p)
	        if form.is_valid():
	            post_edited = form.save()
	            return HttpResponseRedirect('/user/%s' % (profileName))
	    else:
	        form = ProfileForm(instance=p)
	    return render_to_response('profile.html', {'form' : form }, context_instance = RequestContext(request))
	return HttpResponse('No profile to edit')

def search(request):
	q = urllib.unquote(request.GET.get('q',''))
	q = q.strip()
	if q != '':
		results = Passion.objects.filter(name__icontains= q)
		total = results.count()
	return render_to_response('results.html', 
		{'results':results, 'total':total, 'passion' : q}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def my_passions(request):
	passions = request.user.get_profile().passions.all()
	return render_to_response('my_passions.html', 
		{'passions':passions}, context_instance = RequestContext(request))


def autocomp(request):
	q = request.GET.get('term', '')
	passions = Passion.objects.filter(name__icontains = q )[:10]
	results = []
	for p in passions:
		p_json = {}
		p_json['id'] = p.id
		p_json['label'] = p.name
		p_json['value'] = p.name
		results.append(p_json)
	data = simplejson.dumps(results)
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
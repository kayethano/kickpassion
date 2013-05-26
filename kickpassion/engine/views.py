from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from kickpassion.engine.models import Passion, Picture
from kickpassion.engine.forms import PassionForm


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

			return HttpResponseRedirect('/')
	else:
		form = PassionForm()
	return render_to_response('passion.html', 
		{'form':form}, context_instance=RequestContext(request))

def view_passion(request, passionID):
	passion = get_object_or_404(Passion, pk=passionID)
	return render_to_response('view_passion.html',
		{'passion':passion}, context_instance=RequestContext(request))


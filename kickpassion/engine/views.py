from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from kickpassion.engine.models import Passion

@login_required(login_url='/login/')
def passion(request):
	if request.method == 'POST':
		form = PassionForm(request.POST)
		if form.is_valid():
			passion = form.save(commit=False)
			passion.owner = request.user
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


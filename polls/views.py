from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Choices, Poll

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		"""Return the last five published polls. (not including those set to be
		published in the future)
		"""
		return Poll.objects.filter(
			pub_date__lte=timezone.now()
			).order_by('-pub_date')[:5]
		

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'

	def get_queryset(self):
		"""
		Excludes any polls that aren't published yet
		"""
		return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultView(generic.DetailView):
	model = Poll
	template_name = 'polls/result.html'

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk = poll_id)
	try:
		selected_choice = p.choices_set.get(pk=request.POST['choice'])
	except (KeyError, Choices.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll': p,
			'error_message': "You didn't select a choice.",
		})
		
	else:
		selected_choice.votes += 1
		selected_choice.save()

		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
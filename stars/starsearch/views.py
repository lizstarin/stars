from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .forms import RepoForm
import requests

def index(request):
	form = RepoForm()
	return render(request, 'starsearch/index.html', {'form': form, 'results_class': 'hide'})

def get_stars(request):
	try:
		form = RepoForm(request.GET)
		if form.is_valid():
			template = loader.get_template('starsearch/index.html')

			r1_stats = get_repo_stats(request, 'repo_one')
			r2_stats = get_repo_stats(request, 'repo_two')

			if r1_stats['header'] == r2_stats['header']:
				winner = "you entered the same repo twice, ya cheater"
			elif r1_stats['stars'] > r2_stats['stars']:
				winner = r1_stats['header']
			elif r2_stats['stars'] > r1_stats['stars']:
				winner = r2_stats['header']
			else:
				winner = "it's a tie!"

			context = RequestContext(request, {
				'form': form,
				'results_class': '',
				'repo_one_stats': get_repo_stats(request, 'repo_one'),
				'repo_two_stats': get_repo_stats(request, 'repo_two'),
				'winner': winner
			})
			return HttpResponse(template.render(context))
		else:
			return render(request, 'starsearch/index.html', {'form': form, 'results_class': 'hide'})
	except KeyError:
		return render(request, 'starsearch/index.html', {'form': form, 'results_class': 'hide'})

def get_repo_stats(request, repo):
	base_url = 'https://api.github.com/repos/'
	repo_slug = request.GET.get(repo).split('https://github.com/').pop()
	
	stats = requests.get(base_url + repo_slug).json()
	return {'stars': stats['stargazers_count'], 'watchers': stats['subscribers_count'], 'forks': stats['forks'], 'header': repo_slug}
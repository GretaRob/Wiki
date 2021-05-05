from django.shortcuts import render

from . import util
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, 'encyclopedia/entry.html', {
        'content': markdown2.markdown(util.get_entry(title)), 'title': title
    })


def search(request):
    search = request.GET.get('q', '')
    entries = util.list_entries()
    if search:
        # if search query matches one of the entries
        return HttpResponseRedirect(reverse('entry', kwargs={'title': search}))
    else:
        results = []
        for entry in entries:
            if search in entry:
                results.append(entry)

        return render(request, 'encyclopedia/search.html', {
            'results': results
        })

from django.shortcuts import render
from django.contrib import messages
from . import util
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms


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


class NewEntryForm(forms.Form):
    entry = forms.CharField(label='New Entry')
    content = forms.CharField(widget=forms.Textarea(), label='')


def create(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # Isolate the entry from the 'cleaned' version of form data
            entry = form.cleaned_data["entry"]
            content = form.cleaned_data['content']
            entries = util.list_entries()

            if entry in entries:
                messages.add_message(
                    request, messages.ERROR, 'The page already exists')
                return render(request, 'encyclopedia/create.html', {'form': form})

            else:
                util.save_entry(entry, content)

                return render(request, 'encyclopedia/entry.html', {
                    'content': markdown2.markdown(util.get_entry(entry))})

        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "create.html", {
                "form": form
            })

    return render(request, 'encyclopedia/create.html', {'form': NewEntryForm()})


def edit(request, title):
    if request.method == 'GET':

        content = util.get_entry(entry)
        form = NewEntryForm({'entry': entry, 'content': content})
        return render(request, 'encyclopedia/edit.html', {'form': form, 'entry': entry})

    form = NewEntryForm(request.POST)
    if form.is_valid():
        entry = form.cleaned_data.get('entry')
        content = form.cleaned_data.get('content')
        util.save_entry(title=entry, content=content)
        return HttpResponseRedirect(reverse('entry', kwargs={'entry': search}))

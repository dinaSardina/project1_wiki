from django.shortcuts import render, redirect, reverse
import markdown
import random
from django import forms
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from . import util


def index(request):
    """
    View function for home page
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """
    View function for particular entry
    """
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown.markdown(util.get_entry(title))
    })


def random_entry(request):
    """
    View function for random entry
    """
    title = random.choice(util.list_entries())
    return redirect(f"/wiki/{title}")


def search(request):
    """
    View function for search form (from sidebar)
    """
    title = request.POST.get('q')
    if title in util.list_entries():
        return redirect(f"/wiki/{title}")
    else:
        list_result = [el for el in util.list_entries() if title.lower() in el.lower()]
        return render(request, "encyclopedia/search.html", {
            "entries": list_result
        })


class EntryForm(forms.Form):
    """
    Form for create new entry
    """
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        data = self.cleaned_data.get('title')
        if util.get_entry(data):
            raise ValidationError('Invalid title - this title already exist')
        return data


def create_new_page(request):
    """
    View function for create new entry
    """
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            new_content = form.cleaned_data['content']
            util.save_entry(new_title, new_content)
            return HttpResponseRedirect(reverse('entry', args=[new_title]))
        else:
            return render(request, "encyclopedia/create_new_page.html", {
                "form": form
            })
    return render(request, 'encyclopedia/create_new_page.html', {
        'form': EntryForm()
    })


class EditForm(forms.Form):
    """
    Form for edit entry
    """
    content = forms.CharField(widget=forms.Textarea)


def edit_page(request, title):
    """
    View function for edit entry
    """
    content = util.get_entry(title)
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['content']
            util.save_entry(title, new_content)
            return HttpResponseRedirect(reverse('entry', args=[title]))
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "form": form,
                "title": title
            })
    return render(request, 'encyclopedia/edit_page.html', {
        'title': title,
        'form': EditForm(initial={'content': content})
    })
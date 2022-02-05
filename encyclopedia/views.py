from django.shortcuts import render, redirect, reverse
import markdown
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown.markdown(util.get_entry(title))
    })


def random_entry(request):
    title = random.choice(util.list_entries())
    return redirect(f"/wiki/{title}")


def search(request):
    title = request.POST.get('q')
    if title in util.list_entries():
        return redirect(f"/wiki/{title}")
    else:
        list_result = [el for el in util.list_entries() if title.lower() in el.lower()]
        return render(request, "encyclopedia/search.html", {
            "entries": list_result
        })



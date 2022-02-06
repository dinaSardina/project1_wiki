from django.shortcuts import render, redirect, reverse
import markdown
import random
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

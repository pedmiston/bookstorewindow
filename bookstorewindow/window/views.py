from django.shortcuts import render

from .forms import SearchForm


def index(request):
    form = SearchForm()
    return render(request, "window/index.html", {"form": form})

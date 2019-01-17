from django.shortcuts import render
from django.views import View

from .forms import SearchForm
from .models import Book


class WindowView(View):
    template_name = "window/index.html"
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            books = Book.objects.search(query)
            return render(request, self.template_name, {"form": form, "query": query, "books": books})

        return render(request, self.template_name, {"form": form})

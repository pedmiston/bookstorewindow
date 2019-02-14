from django.shortcuts import render
from django.views import View

from .forms import SearchForm
from .models import Book, create_books_from_volume_data

from google_books.api import search_volumes


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
            volume_data = search_volumes(query)
            books = create_books_from_volume_data(volume_data)
            if len(books) == 0:
                form.add_error("query", "No books by that name were found!")
            return render(request, self.template_name, {"form": form, "books": books})

        return render(request, self.template_name, {"form": form})

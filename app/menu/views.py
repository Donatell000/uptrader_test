from django.shortcuts import render, get_object_or_404

from .models import MenuItem


def page_view(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    return render(request, "page.html", {"item": item})


def index_view(request):
    return render(request, "index.html")

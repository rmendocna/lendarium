from django.shortcuts import render

from legends.models import Category
from .models import Article


def index(request):
    categories = Category.objects.filter(parent__isnull=True)  # or level=0 ?
    # current_cat = Category.objects.all()[20]
    content = Article.objects.get(slug_en='archive-of-portuguese-legends')
    return render(request, 'index.html', locals())

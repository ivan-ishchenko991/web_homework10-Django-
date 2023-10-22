from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .forms import AuthorForm, QuoteForm
from .models import Authors, Tag, Quotes


# Create your views here.
def main(request, page=1):
    quotes = Quotes.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quoteapp/index.html', {"quotes": quotes_on_page})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_author.html', {'form': form})

    return render(request, 'quoteapp/add_author.html', {'form': AuthorForm()})
    # return render(request, 'quoteapp/add_author.html')


@login_required
def add_quote(request):
    tags = Tag.objects.all()
    authors = Authors.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            author = Authors.objects.filter(fullname=request.POST.get('author'))[0]
            new_quote.author = author
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_quote.html', {"tags": tags, "authors": authors, "form": form})

    return render(request, 'quoteapp/add_quote.html', {"tags": tags, "authors": authors, "form": QuoteForm()})


def author_info(request, author_name):
    author = Authors.objects.get(fullname=author_name)
    return render(request, 'quoteapp/author.html', {'author': author})

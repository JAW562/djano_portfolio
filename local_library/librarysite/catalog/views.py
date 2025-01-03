from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_genres = Genre.objects.all().count()

    num_foundation_availble = Book.objects.filter(title__contains='Foundation').count()



    num_authors = Author.objects.all().count()

    context = {

        'num_books': num_books,
        'num_genres': num_genres,
        'num_foundation_available' : num_foundation_availble,
        'num_instances' :num_instances,
        'num_instances_available': num_instances_available,
        'num_authors' : num_authors

        
        }


    return render(request, 'index.html', context = context)
from random import choices
from django.db import models
from django.urls import reverse #Used to get the absolute URL
from django.db.models import UniqueConstraint #Constrains field to a unqiue value
from django.db.models.functions import Lower #Returns lower cased value of field
import uuid

# Create your models here.

class Genre(models.Model):

    """ Typical way to define models, deriving from Model class. """

    #Fields
    name = models.CharField(
        max_length = 200, 
        help_text = 'Enter a book genre', 
        unique = True
        )
    
    def __str__ (self):
        
        """ String that represents the object in the Admin Site """

        return self.name

    def get_absolute_url(self):
        
        """ Returns the URL to access a particualr instance of this model. """
        
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:

        """ Further drives that genre must be unique. Checks the name unqiue constraint to make sure, after converting it all to lower case, that it is in fact unique. E.g. Prevents adding History and HIStory as different genres """
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name = "genre_name_case_insenstive_unique",
                violation_error_message = "Genre already exsits."
                )
            ]


class Book(models.Model):
    title = models.CharField(
        max_length = 200,
        help_text = 'Enter title of book'
        )
    """ Restrict does not allow deleting unless the object if the object references a different one that is also being deleted in the same operation. So every book by an author needs to be deleted before an author can be. """
    author = models.ForeignKey('Author', on_delete = models.RESTRICT, null = True)

    summmary = models.TextField(
        max_length = 1000,
        help_text = 'Enter summary of book.'
        )

    ISBN = models.CharField('ISBN',
        max_length= 13,
        unique = True,
        help_text = 'Enter ISBN of book.'
        )

    genre = models.ManyToManyField(Genre, help_text = "Select a genre for this book." )

    language = models.ManyToManyField( 'Language', help_text = "Select a langauge for this book.")

    def __str__ (self):
        
        """ String that represents the object in the Admin Site """

        return self.title


    def display_genre(self):
        return ','.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        
        """ Returns the URL to access a particualr instance of this model. """
        
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):

    #UUID standing for Universally Unique Identifier. Allocates a globally unique value for each instance.
    uniqueId = models.UUIDField(
        primary_key= True,
        default=uuid.uuid4,
        help_text= 'Enter ID of book. Not the same as ISBN.'
        )

    due_back = models.DateField(
        null = True,
        blank = True
        )

    #Tuple defining key and value pairs
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
        )

    status = models.CharField(
        max_length= 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text = "Choose the books availablity"
        )

    book = models.ForeignKey('Book', on_delete=models.RESTRICT, help_text = 'Book that the key applies to.')

    imprint = models.CharField(
        max_length = 200,
        help_text= 'Enter imprint of book.'
    )

    #borrower = models.ForeignKey('User', on_delete = models.RESTRICT, help_text= 'User who has book out.')


    class Meta:
        ordering = ['due_back']

    def __str__ (self):
        
        """ String that represents the object in the Admin Site """
        #Makes a combination of the books ID and title. F strings are Format Strings, just makes it a bit easier to see what you're doing.
        return f'{self.uniqueId} ({self.book.title})'


class Author(models.Model):

    first_name = models.CharField(
        max_length = 100
        )

    last_name = models.CharField(
        max_length = 100
        )

    date_of_birth = models.DateField(
        null = True,
        blank = True
        )

    date_of_death = models.DateField('Died',
        blank = True,
        null = True
        )

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        
        """ Returns the URL to access a particualr instance of this model. """
        
        return reverse('author-detail', args=[str(self.id)])

    def __str__ (self):
        
        """ String that represents the object in the Admin Site """
        #Makes a combination of the books ID and title. F strings are Format Strings, just makes it a bit easier to see what you're doing.
        return f'{self.last_name}, ({self.first_name})'

class Language(models.Model):

  name = models.CharField(
            max_length = 50,
            unique = True
            )

  class Meta:
            constraints = [
                UniqueConstraint(
                    Lower('name'),
                    name = "langauge_name_case_insenstive_unique",
                    violation_error_message = "Language already exsits."
                    )
                ]

  def get_absolute_url(self):
        
        """ Returns the URL to access a particualr instance of this model. """
        
        return reverse('language-detail', args=[str(self.id)])

  def __str__ (self):
        
        """ String that represents the object in the Admin Site """
        #Makes a combination of the books ID and title. F strings are Format Strings, just makes it a bit easier to see what you're doing.
        return self.name















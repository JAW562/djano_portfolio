from django.contrib import admin
from .models import Genre, Book, BookInstance, Author, Language

# Register your models here.
admin.site.register(Genre)
#admin.site.register(Book)
#This does the same thing as the above line
class BookInstanceInline(admin.TabularInline):
    model = BookInstance

    extra = 0

class BookInline(admin.TabularInline):
    model = Book
    extra = 0
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    #Pass means admin behavior is unchanged
    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]

#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'uniqueId')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'uniqueId')
            }),

        ('Availability', {
            'fields': ('status', 'due_back')
            }),
        )
#admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]

admin.site.register(Author,AuthorAdmin)
admin.site.register(Language)

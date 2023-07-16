import random
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.urls import reverse
import re
import markdown

from . import util

# Form class for editing an entry
class EditEntryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 15,
        'cols': 80
        }), label="Edit the contents of the page below", initial="[Page Contents]")

# Form class for a new entry
class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'placeholder': "Title"
        }),
        label="Title:")
    # Uses the django form to get the text area
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Your contents here",
        'rows': 15,
        'cols': 80
        }),
       label="Enter the contents of the page:")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Renders an arbitrary page using mardown.markdown to convert the markdwon to HTML
def page_render(request, page):
    # Try to get page, if markdown.markdown receives a None type (page not found) then redirect to 404 page
    try:
        page_contents = markdown.markdown(util.get_entry(page))
        return render(request, "encyclopedia/page_contents.html", {
            "title": page,
            "contents": page_contents
            })
    except AttributeError:
        return render(request, "encyclopedia/page_not_found.html")

# Search page
def search_page(request):
    # Get the user inputted search
    search_get = request.GET.get("q")
    # Ensure that lowercase inputs find the page (e.g., "css" will get to the CSS page)
    list_of_entries = util.list_entries()
    lower_list = [x.lower() for x in list_of_entries]
    search_low = search_get.lower()

    if search_low in lower_list:
        # This makes sure that the correct formatted page title is usedin as the page kwarg
        # In practice I'd think that this would be stored in an SQL DB otherwise that list is gonna suffer 
        i = lower_list.index(search_low)
        page = list_of_entries[i]
        # Need to add kwargs to specifiy the page
        return HttpResponseRedirect(reverse("wiki:content", kwargs={"page": page}))
    else:
        indices = []
        for i, element in enumerate(list_of_entries):
            if re.search(search_get, element, re.IGNORECASE):
                indices.append(i)
        search_results = [list_of_entries[x] for x in indices]
        return render(request, "encyclopedia/search_page.html", {
            "search_results": search_results
            })

def new_page(request):

    # Get form submitted by user
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        # Validating server side
        if form.is_valid():
            # Get title and text
            title = (form.cleaned_data["title"]).capitalize()
            text = form.cleaned_data["text"]

            # Add a new entry
            if not title in util.list_entries():
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse("wiki:index"))
            else:
                return HttpResponseRedirect(reverse("wiki:already_created", kwargs={"title": title}))

    return render(request, "encyclopedia/new_page.html", {
        "form": NewEntryForm()
        })

def already_created(request, title):
    return render(request, "encyclopedia/already_created.html", {
        "title": title
        })

# Editing a page
def editing_page(request, page):

    # Get updated entry submitted by user
    if request.method == "POST":
        update = EditEntryForm(request.POST)

        # Validating server side
        if update.is_valid():
            # Get updated text
            text = update.cleaned_data["text"]

            # Update the entry
            util.save_entry(page, text)
            return HttpResponseRedirect(reverse("wiki:content", kwargs={"page": page}))


    raw_contents = util.get_entry(page)

    return render(request, "encyclopedia/edit_page.html", {
        "title": page,
        "form": EditEntryForm(initial={'text': raw_contents})
        })

# Random page
def random_page(request):
    choices = util.list_entries()
    choice = random.choice(choices)
    return HttpResponseRedirect(reverse("wiki:content", kwargs={"page": choice}))


   














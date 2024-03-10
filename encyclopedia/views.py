from django.shortcuts import render
from markdown2 import Markdown
from django import forms
import random

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def md_to_html(title):
    markdowner = Markdown()
    content = util.get_entry(title)

    if content == None:
        return None
    else:
        return markdowner.convert(content)


def getEntry(request, title):

    html_raw = md_to_html(title)

    if html_raw == None:
        return render(request, "encyclopedia/error.html", {
            "error": "Requested page doesn't exist."
        })

    else:
        return render(request, "encyclopedia/get.html", {
            "title": title.upper(),
            "content": html_raw,
        })


def search(request):
    if request.method == "POST":
        searchQuery = request.POST['search']

        html_raw = md_to_html(searchQuery)

        if html_raw is not None:
            return render(request, "encyclopedia/get.html", {
                "title": searchQuery.upper(),
                "content": html_raw,
            })
        
        else:
            entries = util.list_entries()
            recommendations = []

            for entry in entries:
                if searchQuery.lower() in entry.lower():
                    recommendations.append(entry)

            if len(recommendations) != 0:
                return render(request, "encyclopedia/search.html", {
                    "entries": recommendations,
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "error": "No matching entries found",
                })
        
def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")

    if request.method == "POST":
        entries = util.list_entries()
        
        title = request.POST['title']
        body = request.POST['body']

        #Input validation
        if title == "" or body == "":
            return render(request, "encyclopedia/error.html", {
                "error": "Invalid Input.",
            })
        
        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/error.html", {
                    "error": "Entry already exists.",
                })
        
        util.save_entry(title, body)
        html_raw = md_to_html(title)

        return render(request, "encyclopedia/get.html", {
            "title": title,
            "content": html_raw,
        })
    


def edit (request):
    if request.method == "POST":
        title = request.POST['entry_title']

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    
    

def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['body']

        util.save_entry(title, content)

        html_raw = md_to_html(title)

        return render(request, "encyclopedia/get.html", {
            "title": title,
            "content": html_raw,
        })
    

def random_entry(request):
    entries = util.list_entries()

    rand_title = random.choice(entries)

    html_raw = md_to_html(rand_title)

    return render(request, "encyclopedia/get.html", {
        "title": rand_title,
        "content": html_raw,
    })
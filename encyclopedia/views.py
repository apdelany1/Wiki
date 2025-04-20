from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from django import forms
from django.shortcuts import redirect
import random

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def easteregg(request):
    return HttpResponse("<h1>🥚</h1><h3>^ Here is your easter egg</h3><br><a href='http://127.0.0.1:8000/'>Click here to get on home</a>")

def page(request, name):
    data = util.get_entry(name)

    if data == None:
        return render(request, "encyclopedia/page.html", {
            "noPage": "The page you are looking for was not found, sorry dude."
        })
    
    convertedMarkdown = markdown2.markdown(data)
    return render(request, "encyclopedia/page.html", {
        "name": name,
        "content": convertedMarkdown
    })

class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search")

def search(request):
    form = NewSearchForm(request.GET) 
    if form.is_valid():
        userInput = form.cleaned_data["search"]
        listOfWikis = util.list_entries()

        for wiki in listOfWikis:
            if wiki.lower() == userInput.lower():
                return redirect("entry", name=wiki)

        matches = []
        for wiki in listOfWikis:
            if userInput.lower() in wiki.lower():
                matches.append(wiki)

        return render(request, "encyclopedia/search.html", {
            "userInput": userInput,
            "results": matches
        })

class NewAddForm(forms.Form):
    
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body")

def add(request):
    if request.method == "POST":
        addition = NewAddForm(request.POST)
        if addition.is_valid():
            entryTitle = addition.cleaned_data["title"]
            entryBody = "# " + entryTitle + "\n" + addition.cleaned_data["body"]
            allWikis = util.list_entries()

            for wiki in allWikis:
                if wiki.lower() == entryTitle.lower():
                    
                    return render(request, "encyclopedia/random.html", {
                        "content": "ERROR: That page already exists, click <a href='http://127.0.0.1:8000/'>here</a> to go back home."
                    })

            util.save_entry(entryTitle, entryBody)
            return redirect("entry", name=entryTitle) 
        else:
            return redirect("add")
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewAddForm()
        })

def edit(request):
    if request.method == "POST":
        pageTitle = request.POST.get("name")
        entryText = util.get_entry(pageTitle)

        lineOne = "# " + pageTitle
        descriptionOnly = entryText.replace(lineOne , "").strip()

        return render(request, "encyclopedia/edit.html", {
            "title": pageTitle,
            "body": descriptionOnly
        })
    
class NewEditForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body")

def saveEdit(request):
    if request.method == "POST":
        editRequest = NewEditForm(request.POST)
        if editRequest.is_valid():
            entryTitle = editRequest.cleaned_data["title"]
            entryBody = "# " + entryTitle + "\n" + editRequest.cleaned_data["body"]
            util.save_entry(entryTitle, entryBody)
            return redirect("entry", name=entryTitle)

def randomPage(request):
    listOfWikis = util.list_entries()
    randomNumber = random.randrange(len(listOfWikis))
    data = listOfWikis[randomNumber]
    return redirect("entry", name=data)


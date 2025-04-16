from django.shortcuts import render
from django.http import HttpResponse
import markdown2


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def slash(request):
    return HttpResponse("Hello CSS")

def page(request, name):
    data = util.get_entry(name)

    #if data no
    if data == None:
        return render(request, "encyclopedia/page.html", {
            "noPage": "The page you are looking for was not found."
        })
    
    #if data yes
    converted_markdown = markdown2.markdown(data)
    return render(request, "encyclopedia/page.html", {
        "name": name,
        "content": converted_markdown
    })
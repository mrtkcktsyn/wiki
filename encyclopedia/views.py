from django.shortcuts import redirect, render
from markdown2 import markdown
from random import randint
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        content = "### Page not found."
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "content": content,
        "title": title
    })


    
def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {
        "entries": util.search(q),
        "q": q
    })


    
def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title == "" and content == "":
            return render(request, "encyclopedia/create.html", {
                "message": "Title and content variable should not be empty.",
                "title": title,
                "content": content
            })
        elif title in util.list_entries():
            return render(request, "encyclopedia/create.html", {
                "message": "Your title is already exist. Try again.",
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")



def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {
            "error": "404 Not Found."
        })
    if request.method == "POST":
        content = request.POST.get('content').strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {
                "message": "Can not save an empty file.",
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {
        "content": content,
        "title": title
    })
    


def random(request):
    entries = util.list_entries()
    random_page = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=random_page)
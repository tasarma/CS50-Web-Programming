from django.shortcuts import render
from django import forms
import markdown2
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice

class MyForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(label="Content",widget=forms.Textarea(attrs={'class':'form-control col-md-8 col-lg-8', 'rows':5}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry):
    content = util.get_entry(entry)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "title" : entry
            })
    
    content = markdown2.markdown(content)
    return render(request, "encyclopedia/exist_entry.html", {
        "title" : entry, "content": content
            })


def search(request):
    query = request.GET.get('q')
    if(util.get_entry(query) != None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': query}))
    
    else:
        sub = []
        for entry in util.list_entries():
            if query.upper() in entry.upper():
                sub.append(entry)

        return render(request, "encyclopedia/index.html", {
            "entries": sub,
            "query": query
        })


def new(request):
    if (request.method == "POST"):
        form = MyForm(request.POST)
        if (form.is_valid()):
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            for name in util.list_entries():
                if (title.upper() == name.upper()):
                    error = f"The title '{title}' is already used."
                    return render(request, "encyclopedia/NewPage.html",{
                        "error": error, 
                        "form": form
                        })

            util.save_entry(title, content)
            return entry_page(request, title)
        
        else:
            return render(request, "encyclopedia/NewPage.html",{
                    "form": form
                    })
    else:
        return render(request, "encyclopedia/NewPage.html",{
                "form": MyForm()
                })

def random(request):
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': choice( util.list_entries())}))

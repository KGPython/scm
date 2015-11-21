from django.http import HttpResponse
from django.template import loader,Context

# Create your views here.
def index(request):
    t = loader.get_template("index.html")
    c = Context({})
    return HttpResponse(t.render(c))
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.views import View
from analytics.models import ClickEvent
from .forms import SubmitUrlForm
from .models import KirrURL
# Create your views here.

def home_view_fbv(request, *arg,**kwargs):
	if request.method=='POST':
		print(request.POST)
	return render(request,"shortener/home.html",{})

class HomeView(View):
	def get(self,request, *arg,**kwargs):
		the_form =SubmitUrlForm()
		context={
			"title":"Submit URL",
			"form":the_form,
		}
		return render(request,"shortener/home.html",context)

	def post(self,request, *arg,**kwargs):
		form =SubmitUrlForm(request.POST)
		context={
			"title":"Submit URL",
			"form":form,
		}
		template="shortener/home.html"
		if form.is_valid():
			new_url=form.cleaned_data.get("url")
			obj,created=KirrURL.objects.get_or_create(url=new_url)
			context={
				"object":obj,
				"created":created,
			}
			if created:
				template="shortener/success.html"
			else:
				template="shortener/already-exists.html"
		return render(request,template,context)
		
class URLRedirectView(View):
	def get(self,request,shortcode=None,*args,**kwargs):
		obj=get_object_or_404(KirrURL,shortcode=shortcode)
		print(ClickEvent.objects.create_event(obj))
		return HttpResponse("class {sc}".format(sc=obj.url))

	
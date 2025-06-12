from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'index.html')



def technology(request):
	return render(request, 'technology.html')

def help_center(request):
	return render(request, 'help_center.html')

def map(requrst):
	return render(requrst, 'map.html')

def order(request):
	return render(request, 'order.html')
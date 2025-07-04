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

def residential(request):
	return render(request, 'residential.html')

def roam(request):
	return render(request, 'roam.html')

def service_plans(request):
	return render(request, 'service_plans.html')

def service_plans_business(request):
	return render(request, 'service_plans_business.html')

def sign_in(request):
	return render(request, 'sign_in.html')

def specifications(request):
	return render(request, 'specifications.html')

def update(request):
	return render(request, 'update.html')

def video_guides(request):
	return render(request, 'video_guides.html')

def index_business(request):
	return render(request, 'index_business.html')

def business_aviation(request):
	return render(request, 'business_aviation.html')

def business_direct_to_cell(request):
	return render(request, 'business_direct_to_cell.html')

def business_fixed_site(request):
	return render(request, 'business_fixed_site.html')

def business_maritime(request):
	return render(request, 'business_maritime.html')

def business_mobility(request):
	return render(request, 'business_mobility.html')
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def video_guides(request):
    return render(request, 'video_guides.html')

def update(request):
    return render(request, 'update.html')

def technology(request):
    return render(request, 'technology.html')

def specifications(request):
    return render(request, 'specifications.html')

def sign_in(request):
    return render(request, 'sign_in.html')

def service_plans(request):
    return render(request, 'service_plans.html')

def service_plans_business(request):
    return render(request, 'service_plans_business.html')

def roam(request):
    return render(request, 'roam.html')

def residential(request):
    return render(request, 'residential.html')

def order(request):
    return render(request, 'order.html')

def map(request):
    return render(request, 'map.html')

def help_center(request):
    return render(request, 'help_center.html')

def business(request):
    return render(request, 'business.html')

def business_mobility(request):
    return render(request, 'business_mobility.html')

def business_maritime(request):
    return render(request, 'business_maritime.html')

def business_fixed_site(request):
    return render(request, 'business_fixed-site.html')

def business_direct_to_cell(request):
    return render(request, 'business_direct-to-cell.html')

def business_aviation(request):
    return render(request, 'business_aviation.html')

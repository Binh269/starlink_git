from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse

# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def video_guides(request):
    return render(request, 'video_guides.html')

def update(request):
    return render(request, 'update.html')

def technology(request):
    return render(request, 'technology.html')

def specifications(request):
    products = Product.objects.filter(msp__startswith='KIT')
    return render(request, 'specifications.html', {'products': products})

def sign_in(request):
    return render(request, 'sign_in.html')

def service_plans(request):
    products = Product.objects.all()
    return render(request, 'service_plans.html', {'products': products})

def service_plans_business(request):
    products = Product.objects.all()
    return render(request, 'service_plans_business.html', {'products': products})

def roam(request):
    products = Product.objects.filter(tensp__icontains='Chuyển vùng')
    return render(request, 'roam.html', {'products': products})

def residential(request):
    products = Product.objects.filter(tensp__icontains='Khu dân cư')
    return render(request, 'residential.html', {'products': products})

def order(request, product_code=None):
    if product_code:
        selected_product = get_object_or_404(Product, msp=product_code)
    else:
        # Default to first product if no code provided
        selected_product = Product.objects.first()
    
    products = Product.objects.all()
    return render(request, 'order.html', {
        'products': products,
        'selected_product': selected_product
    })

def map(request):
    return render(request, 'map.html')

def help_center(request):
    return render(request, 'help_center.html')

def business(request):
    products = Product.objects.all()
    return render(request, 'business.html', {'products': products})

def business_mobility(request):
    products = Product.objects.all()
    return render(request, 'business_mobility.html', {'products': products})

def business_maritime(request):
    products = Product.objects.all()
    return render(request, 'business_maritime.html', {'products': products})

def business_fixed_site(request):
    products = Product.objects.all()
    return render(request, 'business_fixed_site.html', {'products': products})

def business_direct_to_cell(request):
    products = Product.objects.all()
    return render(request, 'business_direct_to_cell.html', {'products': products})

def business_aviation(request):
    products = Product.objects.all()
    return render(request, 'business_aviation.html', {'products': products})

def admin_products(request):
    if not request.user.is_staff:
        return redirect('admin:login')
    products = Product.objects.all()
    return render(request, 'admin.html', {'products': products})

def admin_add_product(request):
    if not request.user.is_staff:
        return redirect('admin:login')
    
    if request.method == 'POST':
        msp = request.POST.get('msp')
        tensp = request.POST.get('tensp')
        gia = request.POST.get('gia')
        mota = request.POST.get('mota')
        
        Product.objects.create(
            msp=msp,
            tensp=tensp,
            gia=gia,
            mota=mota
        )
        messages.success(request, 'Thêm sản phẩm thành công!')
        return redirect('admin_products')
    
    return redirect('admin_products')

def admin_edit_product(request):
    if not request.user.is_staff:
        return redirect('admin:login')
    
    if request.method == 'POST':
        msp = request.POST.get('msp')
        tensp = request.POST.get('tensp')
        gia = request.POST.get('gia')
        mota = request.POST.get('mota')
        
        product = get_object_or_404(Product, msp=msp)
        product.tensp = tensp
        product.gia = gia
        product.mota = mota
        product.save()
        
        messages.success(request, 'Cập nhật sản phẩm thành công!')
        return redirect('admin_products')
    
    return redirect('admin_products')

def admin_delete_product(request):
    if not request.user.is_staff:
        return redirect('admin:login')
    
    if request.method == 'POST':
        msp = request.POST.get('msp')
        product = get_object_or_404(Product, msp=msp)
        product.delete()
        messages.success(request, 'Xóa sản phẩm thành công!')
        return redirect('admin_products')
    
    return redirect('admin_products')

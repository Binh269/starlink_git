from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings

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

def send_to_messenger(order_data):
    """
    Gửi thông tin đơn hàng đến Facebook Messenger
    """
    message = f"""🛒 ĐƠN HÀNG MỚI
👤 Khách hàng: {order_data.get('customer_name')}
📱 Số điện thoại: {order_data.get('phone')}
🛍️ Sản phẩm: {order_data.get('product')}
🔧 Phụ kiện: {order_data.get('accessories', 'Không có')}
💰 Tổng tiền: {order_data.get('total')}
📝 Ghi chú: {order_data.get('notes', 'Không có')}"""

    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={settings.FB_PAGE_ACCESS_TOKEN}"
    
    # ID của page admin hoặc người quản lý page
    recipient_id = "YOUR_ADMIN_ID"  # Thay thế bằng ID của bạn
    
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message}
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Message sent successfully: {message}")
            return True
        else:
            print(f"Failed to send message: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return False

@csrf_exempt
def process_order(request):
    """
    Xử lý đơn hàng và gửi thông tin đến Facebook
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Gửi thông tin đơn hàng đến Facebook
            success = send_to_messenger(data)
            if success:
                return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'error', 'message': 'Failed to send to Facebook'}), 
                                 content_type='application/json', status=500)
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'error', 'message': str(e)}), 
                             content_type='application/json', status=500)
    
    return HttpResponse('Method not allowed', status=405)

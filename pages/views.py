from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)

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
    return render(request, 'business_fixed-site.html', {'products': products})

def business_direct_to_cell(request):
    products = Product.objects.all()
    return render(request, 'business_direct-to-cell.html', {'products': products})

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
    Gửi thông tin đơn hàng qua Facebook API
    """
    # Chuẩn bị dữ liệu đơn hàng
    message = format_order_message(order_data)
    
    # Thử từng phương pháp cho đến khi thành công
    
    # Phương pháp 1: Đăng bài lên trang
    try:
        logger.info(f"Đang thử phương pháp 1: Đăng bài lên trang")
        url = f"https://graph.facebook.com/v18.0/{settings.FB_PAGE_ID}/feed"
        
        params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN,
            "message": message
        }
        
        response = requests.post(url, params=params)
        logger.info(f"Phản hồi phương pháp 1: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            post_id = response.json().get('id')
            logger.info(f"Đã đăng bài thành công, ID: {post_id}")
            return True, None
    except Exception as e:
        logger.warning(f"Lỗi phương pháp 1: {str(e)}")
    
    # Phương pháp 2: Gửi tin nhắn qua Page API
    try:
        logger.info(f"Đang thử phương pháp 2: Gửi tin nhắn qua Page API")
        url = f"https://graph.facebook.com/v18.0/{settings.FB_PAGE_ID}/messages"
        
        params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN
        }
        
        data = {
            "recipient": {
                "id": settings.FB_ADMIN_ID  # ID người nhận (PSID)
            },
            "message": {
                "text": message
            }
        }
        
        response = requests.post(url, json=data, params=params)
        logger.info(f"Phản hồi phương pháp 2: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            message_id = response.json().get('message_id')
            logger.info(f"Đã gửi tin nhắn thành công, ID: {message_id}")
            return True, None
    except Exception as e:
        logger.warning(f"Lỗi phương pháp 2: {str(e)}")
    
    # Nếu tất cả các phương pháp đều thất bại, trả về lỗi
    error_message = "Không thể gửi thông tin đơn hàng qua Facebook API"
    logger.error(error_message)
    return False, error_message

@csrf_exempt
def process_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Đã nhận dữ liệu đơn hàng: {data}")
            
            # Kiểm tra dữ liệu cơ bản
            required_fields = ['customer_name', 'phone', 'product']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                return JsonResponse({
                    "status": "error",
                    "message": f"Thiếu thông tin: {', '.join(missing_fields)}"
                }, status=400)
            
            # Gửi thông tin đơn hàng đến Facebook Messenger
            success, error_message = send_to_messenger(data)
            
            if success:
                return JsonResponse({
                    "status": "success",
                    "message": "Đơn hàng đã được gửi thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất."
                })
            else:
                logger.error(f"Không thể gửi tin nhắn: {error_message}")
                return JsonResponse({
                    "status": "error",
                    "message": f"Không thể gửi thông báo đơn hàng: {error_message}"
                }, status=500)
            
        except json.JSONDecodeError:
            logger.error("Lỗi phân tích dữ liệu JSON")
            return JsonResponse({
                "status": "error",
                "message": "Dữ liệu đơn hàng không hợp lệ"
            }, status=400)
        except Exception as e:
            logger.error(f"Lỗi xử lý đơn hàng: {str(e)}")
            return JsonResponse({
                "status": "error",
                "message": f"Lỗi xử lý đơn hàng: {str(e)}"
            }, status=500)
    
    return JsonResponse({"status": "error", "message": "Phương thức không được phép"}, status=405)

def format_order_message(data):
    """Format đơn hàng thành tin nhắn"""
    return f"""
🔔 *ĐƠN HÀNG MỚI* 🔔

👤 *Thông tin khách hàng:*
   - Tên: {data.get('customer_name', 'N/A')}
   - SĐT: {data.get('phone', 'N/A')}
   - Quốc gia: {data.get('country', 'N/A')}

🛒 *Thông tin đơn hàng:*
   - Sản phẩm: {data.get('product', 'N/A')}
   - Phụ kiện: {data.get('accessories', 'Không có')}
   - Tổng tiền: {data.get('total', 'N/A')}

📝 *Ghi chú:* {data.get('notes', 'Không có')}

⏰ Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""

def send_message(recipient_id: str, message_text: str) -> None:
    """Send message to Facebook user"""
    try:
        url = f"https://graph.facebook.com/v18.0/me/messages"
        params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN
        }
        data = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }
        response = requests.post(url, json=data, params=params)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")

def handle_message(sender_id: str, message_text: str) -> None:
    """Handle incoming Facebook message"""
    try:
        # Echo the message back
        send_message(sender_id, f"Echo: {message_text}")
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")

@csrf_exempt
def webhook(request) -> HttpResponse:
    """Handle Facebook webhook"""
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        if mode and token:
            if mode == 'subscribe' and token == settings.FB_VERIFY_TOKEN:
                logger.info('Webhook verified!')
                return HttpResponse(str(challenge).encode())
            else:
                return HttpResponse(b'Error', status=403)
        
        return HttpResponse(b'Error', status=403)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            logger.info(f"Received webhook data: {data}")
            
            if data.get('object') == 'page':
                for entry in data.get('entry', []):
                    for messaging_event in entry.get('messaging', []):
                        sender_id = messaging_event.get('sender', {}).get('id')
                        message_text = messaging_event.get('message', {}).get('text')
                        
                        if sender_id and message_text:
                            handle_message(sender_id, message_text)
                
                return HttpResponse(b'OK')
            return HttpResponse(b'Error', status=404)
            
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            return HttpResponse(b'Error', status=500)
    
    return HttpResponse(b'Error', status=405)

def test_facebook_connection(request) -> HttpResponse:
    """Test Facebook connection"""
    try:
        # Test connection to Facebook Graph API
        url = "https://graph.facebook.com/v18.0/me"
        params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN,
            "fields": "id,name"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # If successful, return success message
        return HttpResponse(b'Connection successful')
    except Exception as e:
        # If failed, return error message
        return HttpResponse(b'Connection failed')

def simple_test_facebook(request) -> HttpResponse:
    """Simple test for Facebook connection"""
    try:
        # Test connection to Facebook Graph API
        url = "https://graph.facebook.com/v18.0/me"
        params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN,
            "fields": "id,name"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # If successful, return success message
        return HttpResponse(b'Connection successful')
    except Exception as e:
        # If failed, return error message
        return HttpResponse(b'Connection failed')

def check_facebook_info(request) -> HttpResponse:
    """Check Facebook page info"""
    try:
        # Get page info
        url = f"https://graph.facebook.com/v18.0/{settings.FB_PAGE_ID}"
        params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN,
            "fields": "id,name,access_token"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # If successful, return success message
        return HttpResponse(b'Info check successful')
    except Exception as e:
        # If failed, return error message
        return HttpResponse(b'Info check failed')

def get_facebook_pages(request) -> HttpResponse:
    """Get Facebook pages"""
    try:
        # Get pages
        url = "https://graph.facebook.com/v18.0/me/accounts"
        params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # If successful, return success message
        return HttpResponse(b'Pages retrieved successfully')
    except Exception as e:
        # If failed, return error message
        return HttpResponse(b'Failed to retrieve pages')

def get_page_conversations(request) -> HttpResponse:
    """Get page conversations"""
    try:
        # Get conversations
        url = f"https://graph.facebook.com/v18.0/{settings.FB_PAGE_ID}/conversations"
        params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # If successful, return success message
        return HttpResponse(b'Conversations retrieved successfully')
    except Exception as e:
        # If failed, return error message
        return HttpResponse(b'Failed to retrieve conversations')



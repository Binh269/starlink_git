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

@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        # Log các thông tin xác thực
        mode = request.GET.get('hub.mode', '')
        token = request.GET.get('hub.verify_token', '')
        challenge = request.GET.get('hub.challenge', '')
        
        logger.info(f"Webhook verification - Mode: {mode}, Token: {token}, Challenge: {challenge}")
        logger.info(f"Expected token: {settings.FB_VERIFY_TOKEN}")
        
        if mode == 'subscribe' and token == settings.FB_VERIFY_TOKEN:
            logger.info("Webhook verified successfully")
            return HttpResponse(challenge)
        else:
            logger.error("Webhook verification failed")
            return HttpResponse('Error', status=403)
    
    elif request.method == 'POST':
        # Xử lý tin nhắn từ người dùng
        data = json.loads(request.body.decode('utf-8'))
        
        if data['object'] == 'page':
            for entry in data['entry']:
                for messaging_event in entry['messaging']:
                    sender_id = messaging_event['sender']['id']
                    
                    # Kiểm tra nếu có tin nhắn văn bản
                    if 'message' in messaging_event and 'text' in messaging_event['message']:
                        message_text = messaging_event['message']['text']
                        # Xử lý tin nhắn ở đây
                        handle_message(sender_id, message_text)
                        
            return HttpResponse('OK')
        return HttpResponse('Error', status=403)

def handle_message(sender_id, message_text):
    """Xử lý tin nhắn và gửi phản hồi"""
    # Ví dụ đơn giản: gửi lại tin nhắn người dùng đã gửi
    send_message(sender_id, f"Bạn đã gửi: {message_text}")

def send_message(recipient_id, message_text):
    """Gửi tin nhắn đến người dùng qua Facebook Messenger"""
    params = {
        "access_token": settings.FB_PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }
    
    response = requests.post(
        "https://graph.facebook.com/v13.0/me/messages",
        params=params,
        headers=headers,
        json=data
    )
    return response.json()

def test_facebook_connection(request):
    """
    Kiểm tra kết nối với Facebook Messages API
    """
    if not request.user.is_staff:
        return JsonResponse({"status": "error", "message": "Không có quyền truy cập"}, status=403)
    
    try:
        # Kiểm tra thông tin trang
        url = f"https://graph.facebook.com/v18.0/me"
        params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN,
            "fields": "id,name"
        }
        
        logger.info(f"Kiểm tra thông tin người dùng/trang: {url}")
        response = requests.get(url, params=params)
        logger.info(f"Phản hồi: {response.text}")
        
        if response.status_code == 200:
            user_info = response.json()
            
            # Kiểm tra thông tin trang
            page_url = f"https://graph.facebook.com/v18.0/{settings.FB_PAGE_ID}"
            page_params = {
                "access_token": settings.FB_PAGE_ACCESS_TOKEN,
                "fields": "name,id"
            }
            
            logger.info(f"Kiểm tra thông tin trang: {page_url}")
            page_response = requests.get(page_url, params=page_params)
            logger.info(f"Phản hồi trang: {page_response.text}")
            
            page_info = {}
            if page_response.status_code == 200:
                page_info = page_response.json()
            
            # Thử gửi một tin nhắn test đến hộp thư của trang
            test_message = f"Kiểm tra kết nối Facebook Messages API - {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}"
            
            # API endpoint để gửi tin nhắn
            test_url = "https://graph.facebook.com/v18.0/me/messages"
            
            # Dữ liệu tin nhắn - gửi tin nhắn đến chính trang
            test_data = {
                "recipient": {
                    "id": settings.FB_PAGE_ID
                },
                "message": {
                    "text": test_message
                }
            }
            
            test_params = {
                "access_token": settings.FB_PAGE_ACCESS_TOKEN
            }
            
            logger.info(f"Gửi tin nhắn test: {test_url}")
            logger.info(f"Dữ liệu: {test_data}")
            test_response = requests.post(test_url, json=test_data, params=test_params)
            logger.info(f"Phản hồi tin nhắn: {test_response.text}")
            
            if test_response.status_code == 200:
                message_id = test_response.json().get('message_id')
                return JsonResponse({
                    "status": "success",
                    "message": f"Kết nối thành công! Đã gửi tin nhắn test đến hộp thư của trang.",
                    "user_info": user_info,
                    "page_info": page_info,
                    "message_id": message_id
                })
            else:
                error = test_response.json().get('error', {}) if test_response.text else {}
                return JsonResponse({
                    "status": "error",
                    "message": f"Không thể gửi tin nhắn: {error.get('message', 'Lỗi không xác định')}",
                    "error_code": error.get('code'),
                    "error_type": error.get('type'),
                    "user_info": user_info,
                    "page_info": page_info,
                    "suggestion": "Hãy kiểm tra quyền của access token và ID trang."
                })
        else:
            error = response.json().get('error', {}) if response.text else {}
            return JsonResponse({
                "status": "error",
                "message": f"Không thể kết nối đến API: {error.get('message', 'Lỗi không xác định')}",
                "error_code": error.get('code'),
                "error_type": error.get('type')
            })
    except Exception as e:
        logger.error(f"Lỗi: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }, status=500)

def simple_test_facebook(request):
    """
    Kiểm tra kết nối với Facebook API một cách đơn giản
    """
    if not request.user.is_staff:
        return JsonResponse({"status": "error", "message": "Không có quyền truy cập"}, status=403)
    
    try:
        # Kiểm tra thông tin người dùng/trang
        me_url = "https://graph.facebook.com/v18.0/me"
        me_params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN
        }
        
        me_response = requests.get(me_url, params=me_params)
        me_data = me_response.json() if me_response.status_code == 200 else {}
        
        # Thử gửi tin nhắn đơn giản
        message_url = "https://graph.facebook.com/v18.0/me/messages"
        message_params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN
        }
        
        message_data = {
            "recipient": {
                "id": settings.FB_PAGE_ID
            },
            "message": {
                "text": f"Test tin nhắn lúc {datetime.now().strftime('%H:%M:%S')}"
            }
        }
        
        message_response = requests.post(message_url, json=message_data, params=message_params)
        message_result = message_response.json() if message_response.text else {}
        
        # Kết quả tổng hợp
        return JsonResponse({
            "me_status": me_response.status_code,
            "me_data": me_data,
            "message_status": message_response.status_code,
            "message_data": message_result,
            "page_id": settings.FB_PAGE_ID,
            "token_preview": settings.FB_PAGE_ACCESS_TOKEN[:20] + "..." if settings.FB_PAGE_ACCESS_TOKEN else "Not set"
        })
    except Exception as e:
        logger.error(f"Lỗi: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }, status=500)

def check_facebook_info(request):
    """
    Kiểm tra thông tin Facebook mà không yêu cầu quyền admin
    """
    try:
        # Hiển thị thông tin cơ bản
        page_id = settings.FB_PAGE_ID
        token_preview = settings.FB_PAGE_ACCESS_TOKEN[:15] + "..." + settings.FB_PAGE_ACCESS_TOKEN[-5:] if settings.FB_PAGE_ACCESS_TOKEN else "Not set"
        
        # Kiểm tra thông tin người dùng/trang
        me_url = "https://graph.facebook.com/v18.0/me"
        me_params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN
        }
        
        me_response = requests.get(me_url, params=me_params)
        me_status = me_response.status_code
        me_text = me_response.text
        me_data = me_response.json() if me_response.status_code == 200 and me_response.text else {}
        
        # Kiểm tra thông tin trang
        page_url = f"https://graph.facebook.com/v18.0/{settings.FB_PAGE_ID}"
        page_params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN
        }
        
        page_response = requests.get(page_url, params=page_params)
        page_status = page_response.status_code
        page_text = page_response.text
        page_data = page_response.json() if page_response.status_code == 200 and page_response.text else {}
        
        # Trả về kết quả dưới dạng HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Kiểm tra thông tin Facebook</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .info-box {{ background-color: #f5f5f5; padding: 15px; margin-bottom: 20px; border-radius: 5px; }}
                .success {{ color: green; }}
                .error {{ color: red; }}
                pre {{ background-color: #eee; padding: 10px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Kiểm tra thông tin Facebook</h1>
                
                <div class="info-box">
                    <h2>Thông tin cấu hình</h2>
                    <p><strong>FB_PAGE_ID:</strong> {page_id}</p>
                    <p><strong>FB_PAGE_ACCESS_TOKEN:</strong> {token_preview}</p>
                </div>
                
                <div class="info-box">
                    <h2>Kiểm tra API /me</h2>
                    <p><strong>Trạng thái:</strong> <span class="{'success' if me_status == 200 else 'error'}">{me_status}</span></p>
                    <p><strong>Kết quả:</strong></p>
                    <pre>{me_text}</pre>
                </div>
                
                <div class="info-box">
                    <h2>Kiểm tra thông tin trang</h2>
                    <p><strong>Trạng thái:</strong> <span class="{'success' if page_status == 200 else 'error'}">{page_status}</span></p>
                    <p><strong>Kết quả:</strong></p>
                    <pre>{page_text}</pre>
                </div>
                
                <div class="info-box">
                    <h2>Kết luận</h2>
                    <p>
                        {'<span class="success">Kết nối API /me thành công!</span>' if me_status == 200 else '<span class="error">Kết nối API /me thất bại!</span>'}
                        <br>
                        {'<span class="success">Kết nối API trang thành công!</span>' if page_status == 200 else '<span class="error">Kết nối API trang thất bại!</span>'}
                    </p>
                    <p><strong>Gợi ý:</strong></p>
                    <ul>
                        {'<li>API /me thành công: Token hợp lệ và đang hoạt động.</li>' if me_status == 200 else '<li>API /me thất bại: Token có thể không hợp lệ hoặc đã hết hạn.</li>'}
                        {'<li>API trang thành công: ID trang hợp lệ và token có quyền truy cập trang.</li>' if page_status == 200 else '<li>API trang thất bại: ID trang có thể không chính xác hoặc token không có quyền truy cập trang.</li>'}
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_content)
    except Exception as e:
        error_message = f"Lỗi: {str(e)}"
        return HttpResponse(f"<h1>Lỗi</h1><p>{error_message}</p>", status=500)

def get_facebook_pages(request):
    """
    Lấy danh sách các trang Facebook mà token hiện tại có quyền truy cập
    """
    try:
        # Lấy danh sách trang từ token
        pages_url = "https://graph.facebook.com/v18.0/me/accounts"
        pages_params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN
        }
        
        pages_response = requests.get(pages_url, params=pages_params)
        pages_data = pages_response.json() if pages_response.status_code == 200 and pages_response.text else {}
        
        # Trả về kết quả dưới dạng HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Danh sách trang Facebook</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .info-box {{ background-color: #f5f5f5; padding: 15px; margin-bottom: 20px; border-radius: 5px; }}
                .success {{ color: green; }}
                .error {{ color: red; }}
                pre {{ background-color: #eee; padding: 10px; overflow-x: auto; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .copy-btn {{ cursor: pointer; background-color: #4CAF50; color: white; border: none; padding: 5px 10px; border-radius: 3px; }}
            </style>
            <script>
                function copyToClipboard(text) {{
                    navigator.clipboard.writeText(text).then(function() {{
                        alert('ID đã được sao chép!');
                    }}, function(err) {{
                        alert('Không thể sao chép: ' + err);
                    }});
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Danh sách trang Facebook</h1>
                
                <div class="info-box">
                    <h2>Thông tin token</h2>
                    <p><strong>Trạng thái API:</strong> <span class="{'success' if pages_response.status_code == 200 else 'error'}">{pages_response.status_code}</span></p>
                </div>
                
                <div class="info-box">
                    <h2>Danh sách trang có thể truy cập</h2>
        """
        
        if pages_response.status_code == 200 and 'data' in pages_data and pages_data['data']:
            html_content += """
                    <table>
                        <tr>
                            <th>Tên trang</th>
                            <th>ID trang</th>
                            <th>Hành động</th>
                        </tr>
            """
            
            for page in pages_data['data']:
                html_content += f"""
                        <tr>
                            <td>{page.get('name', 'N/A')}</td>
                            <td>{page.get('id', 'N/A')}</td>
                            <td><button class="copy-btn" onclick="copyToClipboard('{page.get('id', '')}')">Sao chép ID</button></td>
                        </tr>
                """
            
            html_content += """
                    </table>
                    <p class="success">Tìm thấy các trang mà token có quyền truy cập!</p>
                    <p><strong>Hướng dẫn:</strong></p>
                    <ol>
                        <li>Sao chép ID của trang bạn muốn sử dụng</li>
                        <li>Cập nhật FB_PAGE_ID trong file settings.py</li>
                        <li>Khởi động lại server</li>
                    </ol>
            """
        else:
            html_content += f"""
                    <p class="error">Không tìm thấy trang nào hoặc token không có quyền truy cập danh sách trang!</p>
                    <p>Phản hồi API:</p>
                    <pre>{pages_response.text}</pre>
                    <p><strong>Gợi ý:</strong></p>
                    <ul>
                        <li>Đảm bảo token có quyền "pages_show_list" và "pages_read_engagement"</li>
                        <li>Đảm bảo tài khoản của bạn là admin hoặc editor của ít nhất một trang</li>
                        <li>Thử tạo token mới với đầy đủ quyền</li>
                    </ul>
            """
        
        html_content += """
                </div>
                
                <div class="info-box">
                    <h2>Cấu hình hiện tại</h2>
                    <p><strong>FB_PAGE_ID hiện tại:</strong> """ + settings.FB_PAGE_ID + """</p>
                    <p><strong>Hướng dẫn cập nhật FB_PAGE_ID:</strong></p>
                    <ol>
                        <li>Mở file settings.py</li>
                        <li>Tìm dòng FB_PAGE_ID = '...'</li>
                        <li>Thay thế bằng ID trang mới</li>
                        <li>Lưu file và khởi động lại server</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_content)
    except Exception as e:
        error_message = f"Lỗi: {str(e)}"
        return HttpResponse(f"<h1>Lỗi</h1><p>{error_message}</p>", status=500)

def get_page_conversations(request):
    """
    Lấy danh sách các cuộc hội thoại của trang để tìm PSID
    """
    if not request.user.is_staff:
        return JsonResponse({"status": "error", "message": "Không có quyền truy cập"}, status=403)
    
    try:
        # Lấy danh sách cuộc hội thoại
        conversations_url = f"https://graph.facebook.com/v18.0/{settings.FB_PAGE_ID}/conversations"
        conversations_params = {
            "access_token": settings.FB_PAGE_ACCESS_TOKEN,
            "fields": "participants,link,updated_time"
        }
        
        conversations_response = requests.get(conversations_url, params=conversations_params)
        conversations_data = conversations_response.json() if conversations_response.status_code == 200 else {}
        
        # Trả về kết quả dưới dạng HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Danh sách cuộc hội thoại</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .info-box {{ background-color: #f5f5f5; padding: 15px; margin-bottom: 20px; border-radius: 5px; }}
                .success {{ color: green; }}
                .error {{ color: red; }}
                pre {{ background-color: #eee; padding: 10px; overflow-x: auto; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .copy-btn {{ cursor: pointer; background-color: #4CAF50; color: white; border: none; padding: 5px 10px; border-radius: 3px; }}
            </style>
            <script>
                function copyToClipboard(text) {{
                    navigator.clipboard.writeText(text).then(function() {{
                        alert('ID đã được sao chép!');
                    }}, function(err) {{
                        alert('Không thể sao chép: ' + err);
                    }});
                }}
                
                function updateAdminId(psid) {{
                    document.getElementById('admin_id').value = psid;
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Danh sách cuộc hội thoại</h1>
                
                <div class="info-box">
                    <h2>Thông tin API</h2>
                    <p><strong>Trạng thái API:</strong> <span class="{'success' if conversations_response.status_code == 200 else 'error'}">{conversations_response.status_code}</span></p>
                    <p><strong>Page ID:</strong> {settings.FB_PAGE_ID}</p>
                </div>
        """
        
        if conversations_response.status_code == 200 and 'data' in conversations_data and conversations_data['data']:
            html_content += """
                <div class="info-box">
                    <h2>Danh sách cuộc hội thoại</h2>
                    <table>
                        <tr>
                            <th>Người tham gia</th>
                            <th>PSID</th>
                            <th>Thời gian cập nhật</th>
                            <th>Hành động</th>
                        </tr>
            """
            
            for conversation in conversations_data['data']:
                participants = conversation.get('participants', {}).get('data', [])
                for participant in participants:
                    if participant.get('id') != settings.FB_PAGE_ID:  # Không hiển thị chính trang
                        html_content += f"""
                        <tr>
                            <td>{participant.get('name', 'N/A')}</td>
                            <td>{participant.get('id', 'N/A')}</td>
                            <td>{conversation.get('updated_time', 'N/A')}</td>
                            <td>
                                <button class="copy-btn" onclick="copyToClipboard('{participant.get('id', '')}')">Sao chép ID</button>
                                <button class="copy-btn" onclick="updateAdminId('{participant.get('id', '')}')">Dùng làm Admin ID</button>
                            </td>
                        </tr>
                        """
            
            html_content += """
                    </table>
                </div>
            """
        else:
            html_content += f"""
                <div class="info-box">
                    <h2>Không tìm thấy cuộc hội thoại</h2>
                    <p class="error">Không tìm thấy cuộc hội thoại nào hoặc token không có quyền truy cập!</p>
                    <p>Phản hồi API:</p>
                    <pre>{conversations_response.text}</pre>
                    <p><strong>Gợi ý:</strong></p>
                    <ul>
                        <li>Đảm bảo token có quyền "pages_messaging" và "pages_read_engagement"</li>
                        <li>Đảm bảo trang của bạn đã có ít nhất một cuộc hội thoại</li>
                        <li>Thử nhắn tin cho trang của bạn để tạo cuộc hội thoại mới</li>
                    </ul>
                </div>
            """
        
        html_content += """
                <div class="info-box">
                    <h2>Cập nhật FB_ADMIN_ID</h2>
                    <p>Sao chép ID từ bảng trên và dán vào đây:</p>
                    <form id="update_form">
                        <input type="text" id="admin_id" placeholder="Nhập PSID..." style="width: 300px; padding: 8px;">
                        <p>Sau đó, cập nhật FB_ADMIN_ID trong file settings.py:</p>
                        <pre>FB_ADMIN_ID = '<span id="admin_id_display"></span>'  # ID của admin nhận tin nhắn</pre>
                        <script>
                            document.getElementById('admin_id').addEventListener('input', function() {
                                document.getElementById('admin_id_display').textContent = this.value;
                            });
                        </script>
                    </form>
                </div>
                
                <div class="info-box">
                    <h2>Hướng dẫn tạo cuộc hội thoại mới</h2>
                    <p>Nếu không thấy cuộc hội thoại nào, hãy làm theo các bước sau:</p>
                    <ol>
                        <li>Truy cập trang Facebook của bạn</li>
                        <li>Nhấp vào nút "Nhắn tin" hoặc "Message"</li>
                        <li>Gửi một tin nhắn đến trang</li>
                        <li>Quay lại trang này và làm mới để xem PSID của bạn</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_content)
    except Exception as e:
        error_message = f"Lỗi: {str(e)}"
        return HttpResponse(f"<h1>Lỗi</h1><p>{error_message}</p>", status=500)



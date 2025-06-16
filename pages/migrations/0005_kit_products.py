from django.db import migrations

def add_kit_data(apps, schema_editor):
    Product = apps.get_model('pages', 'Product')
    
    products = [
        {
            'msp': 'KIT001',
            'tensp': 'STARLINK V3 GEN 3 STANDARD KIT',
            'gia': 20000000,
            'mota': 'Bộ tiêu chuẩn được thiết kế cho các doanh nghiệp nhỏ và các ứng dụng internet hàng ngày. Bộ tiêu chuẩn của bạn bao gồm mọi thứ bạn cần để kết nối internet trong vài phút, bao gồm nguồn điện, bộ định tuyến WiFi và đế. Thiết lập này lý tưởng cho những người dùng có ý định sử dụng bộ định tuyến WiFi do Starlink cung cấp. Chúng tôi không thể đảm bảo hiệu suất hoặc khả năng tương thích của Bộ tiêu chuẩn với thiết bị mạng của bên thứ ba.'
        },
        {
            'msp': 'KIT002',
            'tensp': 'STARLINK MINI KIT',
            'gia': 30000000,
            'mota': 'Thông số kỹ thuật:\nKích thước: 28,9 x 24,8 cm (nhỏ hơn một nửa so với Starlink V4)\nTrọng lượng: Khoảng 1 kg\nTốc độ tải xuống: Trên 100 Mbps\nTốc độ tải lên: Khoảng 11.5 Mbps\nĐộ trễ: Khoảng 23 ms\nNguồn điện: USB-C PD, tối thiểu 100W (20V/5A)\nKhả năng tương thích pin sạc dự phòng: Có thể hoạt động với pin sạc dự phòng Anker Prime 27,650mAh (99.54Wh) trong 2-3 giờ.'
        },
        {
            'msp': 'KIT003',
            'tensp': 'STARLINK FLAT HIGH PERFORMANCE',
            'gia': 120000000,
            'mota': 'Flat High Performance Starlink được thiết kế để sử dụng khi đang di chuyển và trong môi trường thời tiết khắc nghiệt. Bộ sản phẩm bao gồm một giá đỡ hình nêm để lắp đặt cố định. Đây là loại đĩa duy nhất được phép sử dụng khi đang di chuyển.'
        }
    ]
    
    for product in products:
        Product.objects.create(**product)

class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0004_aviation_products'),
    ]

    operations = [
        migrations.RunPython(add_kit_data),
    ] 
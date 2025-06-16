from django.db import migrations

def add_initial_data(apps, schema_editor):
    Product = apps.get_model('pages', 'Product')
    
    products = [
        {
            'msp': 'KDC001',
            'tensp': 'Khu dân cư nhỏ',
            'gia': 3500000,
            'mota': 'Người dùng gói Residential Lite sẽ được ưu tiên sau gói Residential và sẽ trải nghiệm tốc độ chậm hơn vào giờ cao điểm. Gói Residential Lite không có sẵn ở tất cả các khu vực. Xem khu vực hỗ trợ tại đây.'
        },
        {
            'msp': 'KDC002',
            'tensp': 'Khu dân cư',
            'gia': 15000000,
            'mota': 'Gói Residential cung cấp tốc độ cao và ổn định cho các hộ gia đình.'
        },
        {
            'msp': 'CV001',
            'tensp': 'Chuyển vùng - 50GB',
            'gia': 3500000,
            'mota': 'Người dùng gói Roam 50 GB bị giới hạn dung lượng 50 GB và có thể trả thêm theo GB nếu muốn dùng thêm dữ liệu.'
        },
        {
            'msp': 'CV002',
            'tensp': 'Chuyển vùng - Không giới hạn',
            'gia': 15000000,
            'mota': 'Gói Roam không giới hạn cho phép bạn sử dụng không giới hạn dữ liệu khi di chuyển.'
        }
    ]
    
    for product_data in products:
        Product.objects.create(**product_data)

def remove_initial_data(apps, schema_editor):
    Product = apps.get_model('pages', 'Product')
    Product.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ] 
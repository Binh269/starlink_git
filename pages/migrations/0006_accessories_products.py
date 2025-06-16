from django.db import migrations

def add_accessories_data(apps, schema_editor):
    Product = apps.get_model('pages', 'Product')
    
    products = [
        {
            'msp': 'ACC001',
            'tensp': 'Đế gắn trên nóc xe',
            'gia': 4000000,
            'mota': 'Đế gắn trên nóc xe cho Starlink'
        },
        {
            'msp': 'ACC002',
            'tensp': 'Đế di động',
            'gia': 3000000,
            'mota': 'Đế di động cho Starlink'
        },
        {
            'msp': 'ACC003',
            'tensp': 'Bộ định tuyến Mini',
            'gia': 10000000,
            'mota': 'Bộ định tuyến Mini cho Starlink'
        },
        {
            'msp': 'ACC004',
            'tensp': 'Ethernet Adapter',
            'gia': 500000,
            'mota': 'Bộ chuyển đổi Ethernet cho Starlink'
        },
        {
            'msp': 'ACC005',
            'tensp': 'Wall Mount',
            'gia': 800000,
            'mota': 'Giá treo tường cho Starlink'
        },
        {
            'msp': 'ACC006',
            'tensp': 'Long Cable (30m)',
            'gia': 1500000,
            'mota': 'Cáp dài 30m cho Starlink'
        },
        {
            'msp': 'ACC007',
            'tensp': 'Short Wall Mount',
            'gia': 600000,
            'mota': 'Giá treo tường ngắn cho Starlink'
        },
        {
            'msp': 'ACC008',
            'tensp': 'Pivot Mount',
            'gia': 1000000,
            'mota': 'Giá đỡ xoay cho Starlink'
        },
        {
            'msp': 'ACC009',
            'tensp': 'Mesh WiFi Router',
            'gia': 3000000,
            'mota': 'Bộ định tuyến WiFi Mesh cho Starlink'
        }
    ]
    
    for product in products:
        Product.objects.create(**product)

def remove_accessories_data(apps, schema_editor):
    Product = apps.get_model('pages', 'Product')
    Product.objects.filter(msp__startswith='ACC').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0005_kit_products'),
    ]

    operations = [
        migrations.RunPython(add_accessories_data, remove_accessories_data),
    ] 
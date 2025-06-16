from django.db import migrations

def add_aviation_data(apps, schema_editor):
    Product = apps.get_model('pages', 'Product')
    
    products = [
        {
            'msp': 'HK001',
            'tensp': 'Doanh nghiệp hàng không - Tiêu chuẩn',
            'gia': 80000000,
            'mota': 'Gói doanh nghiệp hàng không tiêu chuẩn với dữ liệu 20GB/tháng'
        },
        {
            'msp': 'HK002',
            'tensp': 'Doanh nghiệp hàng không - Cao cấp',
            'gia': 50000000,
            'mota': 'Gói doanh nghiệp hàng không cao cấp với dữ liệu không giới hạn'
        }
    ]
    
    for product in products:
        Product.objects.create(**product)

class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0003_business_products'),
    ]

    operations = [
        migrations.RunPython(add_aviation_data),
    ] 
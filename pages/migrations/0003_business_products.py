from django.db import migrations

def add_business_data(apps, schema_editor):
    Product = apps.get_model('pages', 'Product')
    
    products = [
        {
            'msp': 'DNL001',
            'tensp': 'Doanh nghiệp địa phương - 50GB',
            'gia': 15000000,
            'mota': 'Gói doanh nghiệp địa phương 50GB phù hợp cho các doanh nghiệp nhỏ với nhu cầu sử dụng internet vừa phải.'
        },
        {
            'msp': 'DNL002',
            'tensp': 'Doanh nghiệp địa phương - 1TB',
            'gia': 35000000,
            'mota': 'Gói doanh nghiệp địa phương 1TB phù hợp cho các doanh nghiệp vừa với nhu cầu sử dụng internet cao.'
        },
        {
            'msp': 'DNL003',
            'tensp': 'Doanh nghiệp địa phương - 5TB',
            'gia': 160000000,
            'mota': 'Gói doanh nghiệp địa phương 5TB phù hợp cho các doanh nghiệp lớn với nhu cầu sử dụng internet rất cao.'
        },
        {
            'msp': 'DNQT001',
            'tensp': 'Doanh nghiệp quốc tế - 50GB',
            'gia': 15000000,
            'mota': 'Gói doanh nghiệp quốc tế 50GB phù hợp cho các doanh nghiệp có nhu cầu kết nối toàn cầu với lưu lượng vừa phải.'
        },
        {
            'msp': 'DNQT002',
            'tensp': 'Doanh nghiệp quốc tế - 1TB',
            'gia': 35000000,
            'mota': 'Gói doanh nghiệp quốc tế 1TB phù hợp cho các doanh nghiệp có nhu cầu kết nối toàn cầu với lưu lượng cao.'
        },
        {
            'msp': 'DNQT003',
            'tensp': 'Doanh nghiệp quốc tế - 2TB',
            'gia': 160000000,
            'mota': 'Gói doanh nghiệp quốc tế 2TB phù hợp cho các doanh nghiệp có nhu cầu kết nối toàn cầu với lưu lượng rất cao.'
        }
    ]
    
    for product_data in products:
        Product.objects.create(**product_data)

def remove_business_data(apps, schema_editor):
    Product = apps.get_model('pages', 'Product')
    Product.objects.filter(msp__startswith='DN').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_initial_data'),
    ]

    operations = [
        migrations.RunPython(add_business_data, remove_business_data),
    ] 
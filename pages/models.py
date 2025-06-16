from django.db import models

# Create your models here.

class Product(models.Model):
    msp = models.CharField(max_length=50, primary_key=True, verbose_name="Mã sản phẩm")
    tensp = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    gia = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá")
    mota = models.TextField(verbose_name="Mô tả")

    def __str__(self):
        return self.tensp

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"

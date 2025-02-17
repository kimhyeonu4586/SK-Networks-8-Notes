from django.db import models

class OrdersStatus(models.TextChoices):
    PENDING = 'PENDING', '결제 대기'
    COMPLETED = 'COMPLETED', '주문 완료'
    SHIPPING = 'SHIPPING', '배송 중'

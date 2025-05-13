from django.db import models
from datetime import datetime

class TransactionHistory(models.Model):
    trade_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=10)
    trans_date = models.DateTimeField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    amount = models.PositiveIntegerField(null=True, blank=True)
    memo = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # 사용자가 날짜만 입력한 경우 (시간 미포함)
        if isinstance(self.trans_date, str):
            self.trans_date = datetime.strptime(self.trans_date, "%Y-%m-%d")

        if isinstance(self.trans_date, datetime):
            if self.trans_date.hour == 0 and self.trans_date.minute == 0 and self.trans_date.second == 0:
                now = datetime.now()
                self.trans_date = self.trans_date.replace(
                    hour=now.hour,
                    minute=now.minute,
                    second=now.second,
                    microsecond=now.microsecond
                )

        # ✅ 형 변환 추가 (정수 or 실수형으로)
        try:
            self.price = int(self.price)
            self.quantity = int(self.quantity)
        except ValueError:
            self.price = float(self.price)
            self.quantity = float(self.quantity)

        self.amount = self.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'transaction_History'
        #managed = False

    def __str__(self):
        return f"[{self.trade_id}] {self.category} - {self.trans_date}"
    
    def total_price(self):
        return self.price * self.quantity


class Trade(models.Model):
    TYPE_CHOICES = [
        ('BUY', '매매'),
        ('SELL', '매도'),
    ]
    trade_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='거래 유형')
    trans_date = models.DateField(verbose_name='거래 날짜')
    price = models.PositiveIntegerField(verbose_name='가격')
    quantity = models.PositiveIntegerField(verbose_name='수량')
    memo = models.TextField(blank=True, null=True, verbose_name='메모')

    @property
    def amount(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.get_trade_type_display()} - {self.trans_date}'
    
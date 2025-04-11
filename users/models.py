from django.db import models


class TransactionHistory(models.Model):
    trade_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=10)
    trans_date  = models.DateField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    memo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'transaction_History'
        managed = False

    def __str__(self):
        return f"[{self.trade_id}] {self.category} - {self.trans_date}"


    class Meta:
        db_table = 'transaction_History'
        managed = False 

    def __str__(self):
        return f"[{self.trade_id}] {self.category} - {self.trans_date}"


class Trade(models.Model):
    TYPE_CHOICES = [
        ('매매', '매매'),
        ('매도', '매도'),
    ]
    trade_id = models.CharField(max_length=10, choices=TYPE_CHOICES)
    trans_date = models.DateField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    memo = models.TextField(blank=True)

    def __str__(self):
        return f'{self.type} - {self.trans_date}'



    


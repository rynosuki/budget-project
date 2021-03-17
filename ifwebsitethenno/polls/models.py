from django.db import models

# Create your models here.
class Income(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    amount = models.IntegerField(default=0)
    contributor = models.CharField(max_length=32)
    source = models.CharField(max_length=20)
    date = models.DateField()

    def __str__(self):
        return self.income_text

class Expenses(models.Model):
    id = models.IntegerField(default=0, primary_key=True, null=False)
    amount = models.IntegerField(default=0)
    contributor = models.CharField(max_length=32)
    source = models.CharField(max_length=20)
    date = models.DateField()
    receiptid = models.IntegerField(null=False)
    type = models.CharField(max_length=20, null=False)
    note = models.CharField(max_length=255)

    def __str__(self):
        return self.expenses_text

class Items(models.Model):
    receiptid = models.IntegerField(null = False)
    name = models.CharField(max_length=20, null=False)
    amount = models.IntegerField(null=False)

    def __str__(self):
        return self.items_text

from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True, null=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} on {}".format(
        self.email,
        self.created_at.strftime('%Y-%m-%m'))

class Transaction(models.Model):
    user = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='creator')
    lender = models.ForeignKey('Person',on_delete=models.CASCADE,related_name='lender')#models.IntegerField(null=False)
    borrower = models.ForeignKey('Person', on_delete=models.CASCADE,related_name='borrower')#models.IntegerField(null=False)
    amount = models.IntegerField(null=False)
    currency = models.CharField(default='INR',null=False,max_length=3)
    created_at = models.TimeField(auto_now_add=True)
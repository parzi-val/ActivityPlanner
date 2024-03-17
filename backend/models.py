from django.db import models

from django.contrib.auth.models import User

class OrderEnlisting(models.Model):
    placer = models.ForeignKey(User,null = True,on_delete=models.SET_NULL)
    id = models.CharField(max_length = 10,primary_key=True)
    vendor = models.CharField(max_length=30)
    orderid = models.CharField(max_length=20)
    place = models.CharField(max_length = 40)
    time = models.TimeField()
    incentive = models.IntegerField()
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
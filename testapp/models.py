from django.db import models

class QueueRequest(models.Model):

    methods_choices = (
        ('POST', 'post'),
        ('GET', 'get'),
        ('OPTIONS', 'options'),
        ('HEAD', 'head'),
        ('DELETE', 'delete'),
        ('PATCH', 'patch'),
        ('PUT', 'put'),
    )

    uri = models.CharField(max_length=2048)
    method = models.CharField(max_length=7)
    params = models.CharField(max_length=2048)
    headers = models.JSONField()
    is_sent = models.BooleanField(default=False)


class QueueResponse(models.Model):
    
    request = models.ForeignKey(to=QueueRequest, on_delete=models.CASCADE, related_name='responses')
    status_code = models.IntegerField()
    body = models.JSONField()


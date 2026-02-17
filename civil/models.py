from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,          # ← string reference, safe even if no custom user
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    boq_output = models.JSONField(null=True, blank=True)   # will store structured result

    def __str__(self):
        return self.name

class BOQItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="boq_items")
    item = models.CharField(max_length=500)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)   # m3, bags, tons, etc.
    unit_rate = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
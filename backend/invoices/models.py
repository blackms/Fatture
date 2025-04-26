from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Invoice(models.Model):
    INVOICE_TYPES = (
        ('expense', 'Expense'),
        ('revenue', 'Revenue'),
    )

    STATUS_CHOICES = (
        ('uploaded', 'Uploaded'),
        ('reviewed', 'Reviewed by Accountant'),
        ('processed', 'Processed by Accountant'),
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES)
    file = models.FileField(
        upload_to='invoices/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'xml'])]
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # For expense invoices
    supplier_name = models.CharField(max_length=255, blank=True, null=True)
    
    # For revenue invoices
    customer_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_invoice_type_display()} - {self.amount} - {self.date}"

class InvoiceComment(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.invoice}" 
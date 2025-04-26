from rest_framework import serializers
from .models import Invoice, InvoiceComment
from users.serializers import UserSerializer

class InvoiceCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = InvoiceComment
        fields = ('id', 'author', 'content', 'created_at')
        read_only_fields = ('id', 'author', 'created_at')

class InvoiceSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    comments = InvoiceCommentSerializer(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('id', 'client', 'invoice_type', 'file', 'file_url', 'amount', 
                 'date', 'description', 'status', 'supplier_name', 'customer_name',
                 'created_at', 'updated_at', 'comments')
        read_only_fields = ('id', 'client', 'created_at', 'updated_at')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url)
        return None

    def validate(self, data):
        if data.get('invoice_type') == 'expense' and not data.get('supplier_name'):
            raise serializers.ValidationError({"supplier_name": "Supplier name is required for expense invoices."})
        if data.get('invoice_type') == 'revenue' and not data.get('customer_name'):
            raise serializers.ValidationError({"customer_name": "Customer name is required for revenue invoices."})
        return data

class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('invoice_type', 'file', 'amount', 'date', 'description',
                 'supplier_name', 'customer_name')

class InvoiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('status', 'description')

class InvoiceCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceComment
        fields = ('content',) 
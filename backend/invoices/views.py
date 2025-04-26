from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Invoice, InvoiceComment
from .serializers import (
    InvoiceSerializer, InvoiceCreateSerializer,
    InvoiceUpdateSerializer, InvoiceCommentSerializer,
    InvoiceCommentCreateSerializer
)

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_accountant:
            # Accountants can see invoices of their clients
            return Invoice.objects.filter(client__in=user.clients.all())
        else:
            # Clients can only see their own invoices
            return Invoice.objects.filter(client=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return InvoiceUpdateSerializer
        return InvoiceSerializer

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        invoice = self.get_object()
        serializer = InvoiceCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(invoice=invoice, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        if user.is_accountant:
            invoices = Invoice.objects.filter(client__in=user.clients.all())
        else:
            invoices = Invoice.objects.filter(client=user)

        # Get date range from query params
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            invoices = invoices.filter(date__range=[start_date, end_date])
        else:
            # Default to last 30 days
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
            invoices = invoices.filter(date__range=[start_date, end_date])

        # Calculate summaries
        expense_summary = invoices.filter(invoice_type='expense').aggregate(
            total=Sum('amount'),
            count=Count('id')
        )

        revenue_summary = invoices.filter(invoice_type='revenue').aggregate(
            total=Sum('amount'),
            count=Count('id')
        )

        return Response({
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'expenses': expense_summary,
            'revenue': revenue_summary
        })

class InvoiceCommentViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InvoiceComment.objects.filter(
            Q(invoice__client=self.request.user) |
            Q(invoice__client__in=self.request.user.clients.all())
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 
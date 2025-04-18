from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pass
from .forms import PassRequestForm
from django.utils import timezone
from .serializers import PassSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser



def pass_request_view(request):
    if request.method == 'POST':
        form = PassRequestForm(request.POST)
        if form.is_valid():
            pass_request = form.save(commit=False)
            pass_request.status = 'PENDING'
            pass_request.save()
            messages.success(request, 'Your pass request has been submitted successfully!')
            return redirect('passes:pass_request')
    else:
        form = PassRequestForm()

    context = {
        'form': form,
        'current_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    return render(request, 'passes/pass_request.html', context)


class PassViewSet(viewsets.ModelViewSet):
    serializer_class = PassSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        status_filter = self.request.query_params.get('status', 'PENDING')
        return Pass.objects.filter(status=status_filter).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def pending(self, request):
        passes = Pass.objects.filter(status='PENDING').order_by('-created_at')
        serializer = self.get_serializer(passes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def approved(self, request):
        passes = Pass.objects.filter(status='APPROVED').order_by('-processed_at')
        serializer = self.get_serializer(passes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def rejected(self, request):
        passes = Pass.objects.filter(status='REJECTED').order_by('-processed_at')
        serializer = self.get_serializer(passes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        pass_obj = self.get_object()
        if pass_obj.status != 'PENDING':
            return Response(
                {'error': 'This pass is not pending'},
                status=status.HTTP_400_BAD_REQUEST
            )

        pass_obj.status = 'APPROVED'
        pass_obj.processed_at = timezone.now()
        pass_obj.processed_by = request.user
        pass_obj.save()

        serializer = self.get_serializer(pass_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        pass_obj = self.get_object()
        if pass_obj.status != 'PENDING':
            return Response(
                {'error': 'This pass is not pending'},
                status=status.HTTP_400_BAD_REQUEST
            )

        pass_obj.status = 'REJECTED'
        pass_obj.processed_at = timezone.now()
        pass_obj.processed_by = request.user
        pass_obj.save()

        serializer = self.get_serializer(pass_obj)
        return Response(serializer.data)
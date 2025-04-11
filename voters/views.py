from django.shortcuts import render
from django.http import JsonResponse
from .models import Voter, VoterField
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Voter
from .serializers import VoterSerializer




@api_view(['GET'])
def filter_voters(request):
    try:
        # Get filter parameters
        mlc_constituncy = request.GET.get('mlc_constituncy', '')
        assembly = request.GET.get('assembly', '')
        mandal = request.GET.get('mandal', '')
        location = request.GET.get('location', '')

        # Start with all voters
        queryset = Voter.objects.all()

        # Apply filters if they exist
        if mlc_constituncy:
            queryset = queryset.filter(data__contains={'MLC CONSTITUNCY': mlc_constituncy})
        if assembly:
            queryset = queryset.filter(data__contains={'ASSEMBLY': assembly})
        if mandal:
            queryset = queryset.filter(data__contains={'MANDAL': mandal})
        if location:
            queryset = queryset.filter(data__contains={'LOCATION': location})

        # Serialize the filtered data
        serializer = VoterSerializer(queryset, many=True)

        return Response({
            'success': True,
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        })

def voter_list(request):
    voters = Voter.objects.all()
    return JsonResponse({
        'count': voters.count(),
        'fields': list(VoterField.objects.values('name', 'field_type'))
    })




@require_POST
@staff_member_required
def send_notification(request):
    try:
        data = json.loads(request.body)
        type_id = data.get('type_id')
        template_id = data.get('template_id')
        channel_id = data.get('channel_id')
        voter_ids = data.get('voter_ids', [])

        # Add your notification sending logic here
        # This is where you'd implement the actual notification sending

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
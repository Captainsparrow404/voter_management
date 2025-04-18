from rest_framework import serializers
from .models import Pass
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class PassSerializer(serializers.ModelSerializer):
    processed_by = UserSerializer(read_only=True)
    status_display = serializers.SerializerMethodField()
    processed_time = serializers.SerializerMethodField()

    class Meta:
        model = Pass
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'temple',
            'visit_date',
            'num_persons',
            'id_proof_type',
            'id_proof_number',
            'status',
            'status_display',
            'processed_time',
            'processed_by',
        ]

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_processed_time(self, obj):
        if obj.processed_at:
            return obj.processed_at.strftime('%Y-%m-%d %H:%M:%S')
        return None
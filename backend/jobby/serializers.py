from rest_framework import serializers
from .models import Job, PortfolioJobMatch

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id', 
            'platform_name', 
            'platform_job_id', 
            'title', 
            'company', 
            'location', 
            'url', 
            'date_posted',
            'tags',
            'ai_processed_at'
        ]

class PortfolioJobMatchSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    tags = serializers.JSONField(source='job.tags', read_only=True)
    
    class Meta:
        model = PortfolioJobMatch
        fields = [
            'id',
            'portfolio',
            'job',
            'match_score',
            'tags',
            'created_at'
        ]
        read_only_fields = ['portfolio', 'created_at']

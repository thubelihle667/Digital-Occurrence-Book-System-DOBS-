from rest_framework import serializers

class SummarySerializer(serializers.Serializer):
    total = serializers.IntegerField()
    open = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    closed = serializers.IntegerField()
    sev_low = serializers.IntegerField()
    sev_medium = serializers.IntegerField()
    sev_high = serializers.IntegerField()

class TimePointSerializer(serializers.Serializer):
    bucket = serializers.DateTimeField()
    count = serializers.IntegerField()

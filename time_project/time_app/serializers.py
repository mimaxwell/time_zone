from rest_framework import serializers

from .models import TimeZone

class UnixSerializer(serializers.Serializer):
    time = serializers.FloatField()

class UTCSerializer(serializers.Serializer):
    time = serializers.DateTimeField() 

class ZoneTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeZone
        fields = ('name', 'description','utc_offset')

class ZoneTimeNameSerializer(serializers.Serializer):
    time = serializers.DateTimeField()

class ZoneTimeOffsetSerializer(serializers.Serializer):
    time_zone_name = serializers.CharField() 


class ZoneTimeCountriesSerializer(serializers.Serializer):
    description = serializers.CharField()

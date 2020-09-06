#from rest_framework import generics
from rest_framework import views, generics
from rest_framework.response import Response

from .serializers import UnixSerializer, UTCSerializer, ZoneTimeSerializer, ZoneTimeNameSerializer, ZoneTimeOffsetSerializer
from .models import TimeZone
import time
import datetime
import pytz

# Create your views here.
class UnixTime(views.APIView):
    
    def get(self, request):
        unixtime = [{"time": time.time()}]
        results  = UnixSerializer(unixtime, many=True).data
        return Response(results)

class UTCTime(views.APIView):

    def get(self, request):
        utctime = [{"time": datetime.datetime.utcnow()}]
        results = UTCSerializer(utctime, many=True).data
        return Response(results)

#returns all time zones time/zone/
class ZoneTime(generics.ListCreateAPIView):
    queryset = TimeZone.objects.all()
    serializer_class = ZoneTimeSerializer

# want a view that is for individual rows in timezone model
# accessed by pk in path
class ZoneTimeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeZone.objects.all()
    serializer_class = ZoneTimeSerializer

# gets specific row where the timezone name is a url parameter
class ZoneTimeName(generics.ListAPIView):
    serializer_class = ZoneTimeNameSerializer
    def get_queryset(self):
        name = self.kwargs['name']

        # A whole bunch of nasty type conversion
        gmt = TimeZone.objects.filter(name=name).values_list('utc_offset')  
        listgmt = list(gmt)
        stringgmt = ''.join(listgmt[0])
        colon_location = stringgmt.find(":")
        utcoffset_temp = stringgmt[0:colon_location]
        tz = pytz.timezone('Etc/'+utcoffset_temp)

        time = [{"time" : pytz.utc.localize(datetime.datetime.utcnow()).astimezone(tz)}]
        results = ZoneTimeNameSerializer(time, many=True).data
        return results

class ZoneTimeOffset(generics.ListAPIView):
    serializer_class = ZoneTimeOffsetSerializer
    
    #print(queryset)
    def get_queryset(self):
        offset = self.kwargs['offset']
        query = "GMT" + offset + ":00"
        name = TimeZone.objects.filter(utc_offset=query).values_list('name')
        time_zone_name = [{"time_zone_name": ''.join(list(name)[0])}]
        results = ZoneTimeOffsetSerializer(time_zone_name, many=True).data
        return results

# this doesn't have a serializer yet
# endpoint "works" but returns wrong thing
class ZoneTimeCountries(views.APIView):
    def get(self, request):
        utctime = [{"time": datetime.datetime.utcnow()}]
        results = UTCSerializer(utctime, many=True).data
        return Response(results)



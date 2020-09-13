#from rest_framework import generics
from rest_framework import views, generics
from rest_framework.response import Response

from .serializers import UnixSerializer, UTCSerializer, ZoneTimeSerializer, ZoneTimeNameSerializer, ZoneTimeOffsetSerializer, ZoneTimeNameOffsetSerializer, ZoneTimeCountriesSerializer
from .models import TimeZone
import time
import datetime
import pytz

import requests
import json 
import sys

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
# time/zone/7/ 
class ZoneTimeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeZone.objects.all()
    serializer_class = ZoneTimeSerializer

# gets specific row where the timezone name is a url parameter
# ex: /time/zone/EAT
# returns time but not offset
class ZoneTimeName(generics.ListAPIView):
    serializer_class = ZoneTimeNameSerializer

    def get_queryset(self):
        name = self.kwargs['name']

        # A whole bunch of nasty type conversion
        utc = TimeZone.objects.filter(name=name).values_list('utc_offset')
        listutc = list(utc) #convert from query set to list
        stringutc = ''.join(listutc[0]) #convert from list to string
        gmt = stringutc.replace('UTC', 'GMT')
        colon_location = gmt.find(":")
        utcoffset_temp = gmt[0:colon_location]
        
        try: # throws value error if a 0 is not at index 4
            if (utcoffset_temp.index('0',0,5) == 4):
                # remove substring
                new_utcoffset = utcoffset_temp[:4] + utcoffset_temp[5:]
        except ValueError as ve:
            new_utcoffset = utcoffset_temp
        # if it's in the format GMT-03 it needs to be in GMT-3
        # needs to be in the format 'Etc/GMT-3
        # currently in the format UTC-03:00
        tz = pytz.timezone('Etc/'+new_utcoffset)

        time = [{"time" : pytz.utc.localize(datetime.datetime.utcnow()).astimezone(tz)}]
        results = ZoneTimeNameSerializer(time, many=True).data
        return results

# returns timezone name when given an offset
# ex: /time/zone/+07 returns "time_zone_name": "VST"
# +7 or -1 will not work
class ZoneTimeOffset(generics.ListAPIView):
    serializer_class = ZoneTimeOffsetSerializer
    def get_queryset(self):
        offset = self.kwargs['offset']
        print(offset)
        query = "UTC" + offset + ":00"
        name = TimeZone.objects.filter(utc_offset=query).values_list('name')
        time_zone_name = [{"time_zone_name": ''.join(list(name)[0])}]
        results = ZoneTimeOffsetSerializer(time_zone_name, many=True).data
        return results


# this doesn't have a serializer yet
# endpoint "works" but returns wrong thing
# example: /time/zone/BET/countries
class ZoneTimeCountries(views.APIView):
    # TODO explain this 
    sys.stdout.reconfigure(encoding='utf-8')
    #serializer_class = ZoneTimeCountriesSerializer

    def get(self, request, name):
        # ge tthe utc offset associated with name
        # some serious repetetion of self
        #query = "GMT" + offset + ":00"
        offset_queryset = TimeZone.objects.filter(name=name).values_list('utc_offset')
        # offset is in the form of <QuerySet [('GMT-3:00',)]>
        # only need it to be -3:00
        offset_gmt = ''.join(list(offset_queryset)[0])

        response = requests.get('https://restcountries.eu/rest/v2/all')        
        parsed = json.loads(response.text)
    
        # now that I have the offset use that to find the country 
        # names where [entry]["timezones"] has an element that == offset_utc
        # collect those names in a list. return that list

        countries_list = []
        # begin just by returning all country names and their timezones
        #iterate through the entries
        for entry in range(len(parsed)):
            if (offset_gmt in parsed[entry]["timezones"] ):
                countries_list.append(parsed[entry]["name"])


        results = ZoneTimeCountriesSerializer([{"countries": countries_list}], many=True).data
        
        return Response(results)


# from time zone name retunrs offset form utc
# example: /time/zone/VST/offset returns [{"offset": "GMT+7:00"}]
class ZoneTimeNameOffset(generics.ListAPIView):
    serializer_class = ZoneTimeNameOffsetSerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        offset = TimeZone.objects.filter(name=name).values_list('utc_offset')
        offset_value = [{"offset": ''.join(list(offset)[0])}]
        results = ZoneTimeNameOffsetSerializer(offset_value, many=True).data
        return results


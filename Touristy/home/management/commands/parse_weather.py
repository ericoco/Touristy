from django.core.management.base import BaseCommand,CommandError
from home.models import Weather
from datetime import datetime
import urllib2
import json

WEATHER_URL = 'http://api.wunderground.com/api/4aa0f6fa0f9a7077/forecast10day/q/Canada/Vancouver.json'


class Command(BaseCommand):
    help = "Call it with no arguments to save the current weather to the database."

    def handle(self, *args, **options):
        date = datetime.now()
        try:
            obj = Weather.objects.get(date_id=date)
            obj.weather_string = self.urlParser()
            obj.save()
            print "Weather existed!"
        except Weather.DoesNotExist:
            print "Creating new Weather object!"
            obj = Weather(date_id=date, weather_string=self.urlParser())
            obj.save()
        print obj



    def urlParser(self):
        f = urllib2.urlopen(WEATHER_URL)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        forecast_array = parsed_json['forecast']['txt_forecast']['forecastday']
        today_forecast = forecast_array[0]['title'] +": "+ forecast_array[0]['fcttext_metric']
        f.close()
        return today_forecast



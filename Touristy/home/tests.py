from django.test import TestCase, RequestFactory
from home.models import Weather, Popularity
from home.management.commands.parse_weather import Command
from datetime import datetime
from django.core.management import call_command
from django.test import Client
from home.views import index
from django.contrib.auth.models import AnonymousUser, User


# Create your tests here.


class PopularityTestCase(TestCase):
    def setUp(self):
        Popularity.objects.get_or_create(lat=49.0, lng=-123.0, pop='high')


    def test_popularity_created_properly(self):
        pop = Popularity.objects.get(lat=49.0, lng=-123)
        self.assertEqual(str(pop), "high: 49,-123")

class WeatherTestCase(TestCase):
    def setUp(self):
        # Gotta make sure we try to parse the weather!
        call_command('parse_weather')
        

    def test_weather_object_exists(self):
        try:
            weather = Weather.objects.get(date_id=datetime.now()) 
            print "We are good!"
        except:
            self.fail("No exception should have been thrown!")


class ClientTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        call_command('parse_weather')
        self.client = Client()


    def test_page_load_and_empty_popularity_list(self):
        # Issue a GET request.
        response = self.client.get('/home/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['popularity_list']), 0)
 
        

class UserTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        call_command('parse_weather')
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test_user', email='lol@lol.com', password='top_secret') 

    def test_existance_of_history(self):
        request = self.factory.get('/home/')
        
        request.user = self.user

        response = index(request)
        #Ensure the page at least loads.
        self.assertEqual(response.status_code, 200)
        # Since the user is 'logged in' it should have a history clear area!
        if "Clear History" not in str(response):
            fail("Should have had clear history since a user is logged in.")


        # Simulate anon index.
        request.user = AnonymousUser()
        response = index(request)

        if "Clear History" in str(response):
            fail("Should NOT have had clear history since it's an Anon.")



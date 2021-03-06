from django.test import TestCase, RequestFactory
from home.models import Weather, Popularity
from home.management.commands.parse_weather import Command
from datetime import datetime
from django.core.management import call_command
from django.test import Client
from home.views import index
from login.models import Favorite
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



class FavoriteTest(TestCase):
    def setUp(self):
        call_command('parse_weather')
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test_user', email='lol@lol.com', password='top_secret') 
        self.user_2 = User.objects.create_user(
            username='test_user_2', email='lol@lol.com', password='top_secret') 

        self.test_user_favorite = Favorite.objects.get_or_create(user_profile=self.user, place_name="My House", lat=49, lng=-123, content_string="My House")

    def test_favorite_on_one_user_only(self):
        try:
            fav = Favorite.objects.get(user_profile=self.user)
        except:
            self.fail("The object should have been able to be found!! We created it on user...")

	try:
            fav = Favorite.objects.get(user_profile=self.user_2)
            self.fail("User 2 has no favorites, so we should not have been able to get it...")
        except:
            pass

    

        

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from concert.models import Concert, ConcertAttending
from concert.forms import LoginForm
from datetime import date


# Checks that the "index" view uses the right template
# and returns the status code 200
class IndexViewTest(TestCase):
    # This test ensures that the index view is accessible
    # and renders the correct template.
    def test_index_view_renders_correctly(self):
        # Simulate a GET request to the 'index' URL.
        response = self.client.get(reverse('index'))

        # Assert that the HTTP status code is 200 (OK),
        # meaning the page loaded successfully.
        self.assertEqual(response.status_code, 200)

        # Assert that the 'index.html' template was used
        # to render the response.
        self.assertTemplateUsed(response, 'index.html')


# Checks that the "song" view uses the right template,
# returns the status code 200 and passes data
class SongViewTest(TestCase):
    # This test ensures the songs view is accessible, renders the correct
    #  template and passes the expected song data to the template context.
    def test_songs_view_renders_correctly_with_data(self):
        # Simulate a GET request to the 'songs' URL.
        response = self.client.get(reverse('songs'))

        # Assert that the HTTP status code is 200 (OK).
        self.assertEqual(response.status_code, 200)

        # Assert that the 'songs.html' template was used.
        self.assertTemplateUsed(response, 'songs.html')

        # Define the expected static data that the view should pass.
        expected_songs_data = [{
                    "id": 1,
                    "title": "duis faucibus accumsan odio curabitur convallis",
                    "lyrics": ("Morbi non lectus. Aliquam sit "
                               "amet diam in magna bibendum "
                               "imperdiet. Nullam orci pede, "
                               "venenatis non, sodales sed, "
                               "tincidunt eu, felis.")
                            }]

        # Assert that the 'songs' key is present in the template context.
        self.assertIn('songs', response.context)

        # Assert that the data passed under the 'songs' key
        # matches the expected data.
        self.assertEqual(response.context['songs'], expected_songs_data)

        # Assert that specific content from the song data is present
        # in the HTML response. This helps verify that the data is correctly
        # rendered in the template.
        # Check for song title
        self.assertContains(response,
                            "duis faucibus accumsan odio curabitur convallis")

        # Check for part of the lyrics
        self.assertContains(response, "Morbi non lectus.")


# Checks that the "photos" view uses the right template,
# returns the status code 200 and passes data
class PhotosViewTest(TestCase):
    # This test ensures the photos view is accessible, renders the correct
    # template and passes the expected photo data to the template context.
    def test_photos_view_renders_correctly_with_data(self):
        # Simulate a GET request to the 'photos' URL.
        response = self.client.get(reverse('photos'))

        # Assert that the HTTP status code is 200 (OK).
        self.assertEqual(response.status_code, 200)

        # Assert that the 'photos.html' template was used.
        self.assertTemplateUsed(response, 'photos.html')

        # Define the expected static data that the view should pass.
        expected_photos_data = [{
            "id": 1,
            "pic_url": "http://dummyimage.com/136x100.png/5fa2dd/ffffff",
            "event_country": "United States",
            "event_state": "District of Columbia",
            "event_city": "Washington",
            "event_date": "11/16/2022"
        }]

        # Assert that the 'photos' list is present in the template context.
        self.assertIn('photos', response.context)

        # Assert that the 'photos' list contains the expected data.
        self.assertEqual(response.context['photos'], expected_photos_data)

        # Assert that some content from the data is present
        # in the HTML response.
        # Useful to ensure that the data is correctly displayed
        # in the template.
        self.assertContains(response, "Washington")
        self.assertContains(response, "11/16/2022")
        self.assertContains(response, "dummyimage.com")


# Checks that the "login" view uses the right template
# and handles authentication scenarios
class LoginViewTest(TestCase):
    def setUp(self):
        # Create a user for successful login tests
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword123')

    # Tests the initial display of the login form (GET request)
    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('form', response.context)

        # Ensure the form is an instance of LoginForm
        self.assertIsInstance(response.context['form'], LoginForm)

    # Tests successful login with correct credentials (POST request)
    def test_login_view_post_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })

        # Should redirect to the index page upon successful login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

        # Verify that the user is logged in
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'],
                         str(self.user.pk))

    # Tests failed login with incorrect password (POST request)
    def test_login_view_post_incorrect_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })

        # Should re-render the login page with a 200 status (no redirect)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('form', response.context)

        # Verify that the form contains errors
        self.assertFalse(response.context['form'].is_valid())

        # AuthenticationForm puts errors in __all__
        self.assertIn('__all__', response.context['form'].errors)

        # Verify that the user is NOT logged in
        self.assertFalse('_auth_user_id' in self.client.session)

    # Tests failed login with a non-existent username (POST request)
    def test_login_view_post_non_existent_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'nonexistentuser',
            'password': 'anypassword'
        })

        # Should re-render the login page with a 200 status (no redirect)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('form', response.context)

        # Verify that the form contains errors
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('__all__', response.context['form'].errors)

        # Verify that the user is NOT logged in
        self.assertFalse('_auth_user_id' in self.client.session)

        # Optional: Check for a specific error message
        self.assertContains(response,
                            "Please enter a correct username and password.")


# Checks that the "logout" view redirects to the login page
# and logs out the user
class LogoutViewTest(TestCase):
    def setUp(self):
        # Create and log in a user before each test
        # that requires an authenticated user.
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

        # Simulate logging in the user. This is crucial
        # for testing logout functionality.
        self.client.login(username='testuser', password='testpassword')

    # This test ensures that the logout view successfully logs out the user
    # and redirects them to the login page.
    def test_logout_view_redirects_to_login(self):
        # Simulate a GET request to the 'logout' URL.
        response = self.client.get(reverse('logout'))

        # Assert that the HTTP status code is 302 (Found),
        # indicating a redirection.
        self.assertEqual(response.status_code, 302)

        # Assert that the redirection target is the 'login' page.
        self.assertRedirects(response, reverse('login'))

        # Verify that the user is no longer logged in by checking the session.
        # The '_auth_user_id' key should no longer be present in the session.
        self.assertFalse('_auth_user_id' in self.client.session)


# Checks that the "signup" view uses the right template
# and handles user registration scenarios
class SignupViewTest(TestCase):
    # This test ensures that the signup view is accessible
    # and renders the correct form
    # when accessed via a GET request.
    def test_signup_view_get(self):
        # Simulate a GET request to the 'signup' URL.
        response = self.client.get(reverse('signup'))

        # Assert that the HTTP status code is 200 (OK).
        self.assertEqual(response.status_code, 200)

        # Assert that the 'signup.html' template was used.
        self.assertTemplateUsed(response, 'signup.html')

        # Assert that a 'form' object is passed into the template context.
        self.assertIn('form', response.context)

    # This test covers the successful creation of a new user
    # through a valid POST request.
    def test_signup_view_post_new_user(self):
        # Initial check: Ensure no users exist in the database
        # before this test runs.
        self.assertEqual(User.objects.count(), 0)

        # Simulate a POST request to the 'signup' URL
        # with new user credentials.
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password': 'newpassword123'
        })

        # Assert that the view redirects (302) to the 'index' page
        # upon successful signup.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

        # Verify that exactly one new user has been created in the database.
        self.assertEqual(User.objects.count(), 1)

        # Retrieve the newly created user from the database.
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)

        # Verify that the password was correctly hashed and can be checked.
        self.assertTrue(user.check_password('newpassword123'))

        # Verify that the newly created user is automatically logged in.
        self.assertTrue('_auth_user_id' in self.client.session)

    # This test covers the scenario where a user tries to sign up
    # with an existing username.
    def test_signup_view_post_user_exists(self):
        # Create an existing user to simulate a conflict.
        User.objects.create_user(username='existinguser',
                                 password='oldpassword')

        # Ensure that this user is present before the POST request.
        self.assertEqual(User.objects.count(), 1)

        # Simulate a POST request with the existing username
        # and a new password.
        response = self.client.post(reverse('signup'), {
            'username': 'existinguser',
            'password': 'anotherpassword'
        })

        # Assert that the view re-renders the signup page (200 OK)
        # instead of redirecting.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

        # Verify that no new user was created.
        # The user count should remain unchanged.
        self.assertEqual(User.objects.count(), 1)

        # Verify that the user was NOT logged in.
        self.assertFalse('_auth_user_id' in self.client.session)

        # Assert that the response content includes a message
        # indicating the user already exists.
        self.assertContains(response, "User already exists")


# Checks that the "concerts" view requires login
# and correctly displays data when logged in
class ConcertsViewTest(TestCase):
    def setUp(self):
        # Create a test user for login scenarios.
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

        # Create some concert instances for testing data display.
        self.concert1 = Concert.objects.create(
            concert_name="Rock Festival",
            duration=180,
            city="Paris",
            date=date(2025, 8, 15)
        )
        self.concert2 = Concert.objects.create(
            concert_name="Jazz Night",
            duration=120,
            city="Lyon",
            date=date(2025, 9, 10)
        )

        # Create an attending status for one of the concerts for the test user.
        ConcertAttending.objects.create(
            concert=self.concert1,
            user=self.user,
            attending=ConcertAttending.AttendingChoices.ATTENDING
        )

    # This test ensures that an unauthenticated user attempting
    # to access the concerts view
    # is redirected to the login page.
    def test_concerts_view_unauthenticated_redirects(self):
        # Simulate a GET request to the 'concerts' URL without logging in.
        response = self.client.get(reverse('concerts'))

        # Assert that the HTTP status code is 302 (Found),
        # indicating a redirection.
        self.assertEqual(response.status_code, 302)

        # Assert that the redirection target is the 'login' page.
        self.assertRedirects(response, reverse('login'))

    # This test ensures that an authenticated user can access
    # the concert view, that the correct template is used, and that
    # the concert data is passed correctly.
    def test_concerts_view_authenticated_renders_with_data(self):
        # Log in the test user before making the request.
        self.client.force_login(self.user)

        # Simulate a GET request to the 'concerts' URL.
        response = self.client.get(reverse('concerts'))

        # Assert that the HTTP status code is 200 (OK),
        # meaning the page loaded successfully.
        self.assertEqual(response.status_code, 200)

        # Assert that the 'concerts.html' template was used
        # to render the response.
        self.assertTemplateUsed(response, 'concerts.html')

        # Assert that 'concerts' data is present in the template context.
        self.assertIn('concerts', response.context)

        # Verify the structure and content of the 'concerts' list
        # in the context. It should contain a list of dictionaries
        # with 'concert' objects and their 'status'.
        context_concerts = response.context['concerts']
        self.assertEqual(len(context_concerts), 2)  # Expect 2 concerts

        # Sort the context_concerts by concert_name for consistent comparison,
        # as query order might vary
        context_concerts.sort(key=lambda x: x['concert'].concert_name)

        # Check details for concert1 (Rock Festival)
        self.assertEqual(context_concerts[1]['concert'], self.concert1)
        self.assertEqual(context_concerts[1]['status'],
                         ConcertAttending.AttendingChoices.ATTENDING)

        # Check details for concert2 (Jazz Night)
        self.assertEqual(context_concerts[0]['concert'], self.concert2)
        self.assertEqual(context_concerts[0]['status'],
                         ConcertAttending.AttendingChoices.NOTHING)

        # Assert that some concert names and statuses are present
        # in the HTML response.
        self.assertContains(response,
                            self.concert1.concert_name)
        self.assertContains(response,
                            ConcertAttending.AttendingChoices.ATTENDING)
        self.assertContains(response,
                            self.concert2.concert_name)
        self.assertContains(response,
                            ConcertAttending.AttendingChoices.NOTHING)

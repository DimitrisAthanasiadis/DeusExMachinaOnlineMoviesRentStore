from email import header
import unittest
import json
from environs import Env
from src.app import app


env = Env()
env.read_env("config/.env")


class TestOnlineMovieStoreApi(unittest.TestCase):
    def test_get_all_movies(self):
        print("RUNNING TESTS FOR FETCHING ALL MOVIES")
        client = app.test_client(self)

        response = client.get("/movies/")

        response_status_code = response.status_code
        self.assertEqual(response_status_code, 200)

        response_data = json.loads(response.data.decode())
        self.assertTrue("movies" in response_data)
        self.assertTrue(len(response_data.get("movies")) > 0)

    def test_get_movies_by_category(self):
        print("RUNNING TESTS FOR FETCHING MOVIES BY CATEGORY")
        client = app.test_client(self)

        response = client.post(
            "/movies/category",
            data=json.dumps({"category": "Horror"}),
            content_type="application/json",
        )

        response_status_code = response.status_code
        self.assertEqual(response_status_code, 200)

        response_data = json.loads(response.data.decode())
        self.assertTrue("movies" in response_data)
        self.assertTrue(len(response_data.get("movies")) > 0)

    def test_get_movie_info(self):
        print("RUNNING TESTS FOR FETCHING MOVIE INFO")
        client = app.test_client(self)

        response = client.post(
            "/movies/movie_info",
            data=json.dumps({"movie_id": "3"}),
            content_type="application/json",
        )

        response_status_code = response.status_code
        self.assertEqual(response_status_code, 200)

        response_data = json.loads(response.data.decode())
        self.assertTrue("movie" in response_data)
        self.assertTrue(len(list(response_data.get("movie").keys())) > 0)

    def test_get_movies_by_rating(self):
        print("RUNNING TESTS FOR FETCHING MOVIES BY RATING")
        client = app.test_client(self)

        response = client.post(
            "/movies/rating",
            data=json.dumps({"rating": "9"}),
            content_type="application/json",
        )

        response_status_code = response.status_code
        self.assertEqual(response_status_code, 200)

        response_data = json.loads(response.data.decode())
        self.assertTrue("movies" in response_data)
        self.assertTrue(len(response_data.get("movies")) > 0)

    def test_get_movie_rent_info(self):
        print("RUNNING TESTS FOR FETCHING MOVIE RENT INFO")
        client = app.test_client(self)

        response = client.post(
            "/transaction/rent_info",
            data=json.dumps({"movie_id": "3", "days_to_rent": 10}),
            content_type="application/json",
        )

        response_status_code = response.status_code
        self.assertEqual(response_status_code, 200)

        response_data = json.loads(response.data.decode())
        self.assertTrue("days_to_rent" in response_data)
        self.assertTrue("movie" in response_data)
        self.assertTrue(len(list(response_data.get("movie").keys())) > 0)
        self.assertTrue("rent_price" in response_data)

    def test_rent_movie(self):
        print("RUNNING TESTS FOR RENTING MOVIE")
        client = app.test_client(self)

        response = client.post(
            "/transaction/rent",
            data=json.dumps({"user_id": 2, "movie_id": 4, "days_to_rent": 10}),
            headers={
                "X-Access-Token": env.str("SECRET_KEY"),
                "Content-Type": "application/json",
            },
        )

        response_status_code = response.status_code
        self.assertTrue(response_status_code == 200 or response_status_code == 400)

        response_data = json.loads(response.data.decode())
        self.assertTrue("message" in response_data)
        self.assertTrue(
            response_data.get("message") == "Rent transaction successful"
            or response_data.get("message") == "You can't rent this movie."
        ) # i am doing this because the user might want to rent a movie that is already rented but not returned

    def test_get_not_returned_movies(self):
        print("RUNNING TESTS FOR FETCHING NOT RETURNED MOVIES")
        client = app.test_client(self)

        response = client.post(
            "/transaction/get_not_returned_movies",
            data=json.dumps({"user_id": 2}),
            headers={
                "Content-Type": "application/json",
                "X-Access-Token": env.str("SECRET_KEY"),
            },
        )

        response_status_code = response.status_code
        self.assertEqual(response_status_code, 200)

        response_data = json.loads(response.data.decode())
        self.assertTrue(
            len(response_data) > 0
            or (
                response_data.get("message") is not None
                and response_data.get("message") == "All movies are returned and paid"
            )
        )

    def test_get_user_rented_movies(self):
        print("RUNNING TESTS FOR FETCHING USER RENTED MOVIES")
        client = app.test_client(self)

        response = client.post(
            "/transaction/get_rented_movies",
            data=json.dumps({"user_id": 2}),
            headers={
                "Content-Type": "application/json",
                "X-Access-Token": env.str("SECRET_KEY"),
            },
        )

        response_status_code = response.status_code
        self.assertEqual(response_status_code, 200)

        response_data = json.loads(response.data.decode())
        self.assertTrue(len(response_data) > 0)

    def test_pay_movie(self):
        print("RUNNING TESTS FOR PAYING MOVIE")
        client = app.test_client(self)

        """
        we need to get data dynamically in order to test this.
        in order for it to not false fail, we need a movie id
        that is actually rented and not returned. for testing
        purposes i will always pick the first available movie id
        or, if no rented movies are available, i will consider
        that the test is successful if a certain message is
        returned.
        """
        not_returned_movies = client.post(
            "/transaction/get_rented_movies",
            data=json.dumps({"user_id": 2}),
            headers={
                "Content-Type": "application/json",
                "X-Access-Token": env.str("SECRET_KEY"),
            },
        )
        not_returned_movies_data = json.loads(not_returned_movies.data.decode())
        not_returned_movie_id = not_returned_movies_data[0].get(
            "id"
        )  # i will always choose the first movie for testing purposes

        response = client.post(
            "/transaction/pay",
            data=json.dumps(
                {"user_id": 2, "transaction_id": not_returned_movie_id, "euros": 7}
            ),
            headers={
                "X-Access-Token": env.str("SECRET_KEY"),
                "Content-Type": "application/json",
            },
        )

        response_status_code = response.status_code
        self.assertTrue(
            response_status_code == 200 or response_status_code == 400
        )  # either 200 or 400 because the user might not have movies that were not returned

        response_data = json.loads(response.data.decode())
        self.assertTrue(len(response_data) > 0)
        self.assertTrue(
            ("returned" in response_data and response_data.get("returned") is True)
            or (
                "message" in response_data
                and response_data.get("message")
                == "You haven't rented this movie or you have already paid for it in the last transaction."
            )
        )

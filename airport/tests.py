from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from airport.serializers import (
    CountrySerializer,
    CityWithSlugSerializer,
    AirplaneTypeDetailSerializer,
    AirplaneRetrieveSerializer,
    AirportDetailSerializer,
    RouteWithSlugSerializer,
)
from airport.models import (
    Country,
    City,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Crew,
    Flight,
    Ticket,
    Order,
)

COUNTRY = "country"
CITY = "city"
AIRPLANE_TYPE = "airplane-type"
AIRPLANE = "airplane"
AIRPORT = "airport"
ROUTE = "route"
CREW = "crew"
FLIGHT = "flight"
TICKET = "ticket"
ORDER = "order"


def create_and_return_user(
        username="test",
        email="test@example.com",
        password="test",
        is_staff=True
):
    return get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password,
        is_staff=is_staff
    )


def create_and_return_country(name):
    return Country.objects.create(name=name)


def create_and_return_city(city_name, country_name):
    return City.objects.create(
        name=city_name,
        country=create_and_return_country(country_name)
    )


def create_and_return_airplane_type(name):
    return AirplaneType.objects.create(name=name)


def create_and_return_airplane(airplane_name, airplane_type_name):
    return Airplane.objects.create(
        airplane_type=create_and_return_airplane_type(airplane_type_name),
        name=airplane_name,
        rows=2,
        seats_per_row=4
    )


def create_and_return_airport(airport_name, city_name, country_name):
    return Airport.objects.create(
        name=airport_name,
        closest_big_city=create_and_return_city(city_name, country_name)
    )


def create_and_return_route(source: list, destination: list):
    return Route.objects.create(
        source=create_and_return_airport(*source),
        destination=create_and_return_airport(*destination),
        distance=123
    )


def create_and_return_crew(first_name, last_name):
    return Crew.objects.create(
        first_name=first_name,
        last_name=last_name
    )


def create_and_return_flight(crew: list, route: list, airplane: list):
    flight = Flight.objects.create(
        route=create_and_return_route(*route),
        airplane=create_and_return_airplane(*airplane),
        departure_time="2021-01-01T00:00:00Z",
        arrival_time="2021-01-01T00:00:00Z",
    )
    flight.crew.add(create_and_return_crew(*crew))
    flight.save()
    return flight


def create_and_return_order(user):
    return Order.objects.create(
        user=user
    )


def create_and_return_ticket(user, flight: list, row=1, seat=1):
    return Ticket.objects.create(
        order=create_and_return_order(user),
        flight=create_and_return_flight(*flight),
        row=1,
        seat=1
    )


class TestCountry(APITestCase):
    def test_list(self):
        create_and_return_country("test")
        create_and_return_country("test1")
        create_and_return_country("test2")
        url = reverse(f"airport:{COUNTRY}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        url = reverse(f"airport:{COUNTRY}-list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_detail(self):
        country = Country.objects.create(name="test")
        url = reverse(f"airport:{COUNTRY}-detail", kwargs={"pk": country.pk})
        response = self.client.get(url)
        self.assertEqual(response.json(), CountrySerializer(country).data)

    def test_destroy(self):
        country = Country.objects.create(name="test")
        url = reverse(f"airport:{COUNTRY}-detail", kwargs={"pk": country.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        country = Country.objects.create(name="test")
        url = reverse(f"airport:{COUNTRY}-detail", kwargs={"pk": country.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)


class TestCountryAuth(APITestCase):
    def setUp(self):
        user = create_and_return_user()
        self.client.force_authenticate(user)

    def test_post(self):
        data = {"name": "test"}
        url = reverse(f"airport:{COUNTRY}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Country.objects.count(), 1)
        self.assertEqual(Country.objects.first().name, "test")

    def test_destroy(self):
        country = create_and_return_country("test")
        url = reverse(f"airport:{COUNTRY}-detail", kwargs={"pk": country.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Country.objects.count(), 0)

    def test_update(self):
        country = create_and_return_country("test")
        data = {"name": "test2"}
        url = reverse(f"airport:{COUNTRY}-detail", kwargs={"pk": country.pk})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Country.objects.get(pk=country.pk).name, "test2")


class TestCity(APITestCase):

    def test_list(self):
        create_and_return_city("test1", "test2")
        create_and_return_city("test2", "test1")
        create_and_return_city("test3", "test3")
        url = reverse(f"airport:{CITY}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        city = create_and_return_city("test1", "test2")
        url = reverse(f"airport:{CITY}-detail", kwargs={"pk": city.pk})
        response = self.client.get(url)
        self.assertEqual(response.json(), CityWithSlugSerializer(city).data)

    def test_create(self):
        url = reverse(f"airport:{CITY}-list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_destroy(self):
        city = create_and_return_city("test1", "test2")
        url = reverse(f"airport:{CITY}-detail", kwargs={"pk": city.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        city = create_and_return_city("test1", "test2")
        url = reverse(f"airport:{CITY}-detail", kwargs={"pk": city.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)


class TestCityAuth(APITestCase):
    def setUp(self):
        user = create_and_return_user()
        self.client.force_authenticate(user)

    def test_post(self):
        data = {"name": "test", "country": create_and_return_country("test").pk}
        url = reverse(f"airport:{CITY}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(City.objects.count(), 1)
        self.assertEqual(City.objects.first().name, "test")

    def test_destroy(self):
        city = create_and_return_city("test1", "test2")
        url = reverse(f"airport:{CITY}-detail", kwargs={"pk": city.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(City.objects.count(), 0)

    def test_update(self):
        city = create_and_return_city("test1", "test2")
        data = {"name": "test2"}
        url = reverse(f"airport:{CITY}-detail", kwargs={"pk": city.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(City.objects.get(pk=city.pk).name, "test2")


class TestAirplaneType(APITestCase):
    def test_list(self):
        create_and_return_airplane_type("test")
        create_and_return_airplane_type("test1")
        create_and_return_airplane_type("test2")
        url = reverse(f"airport:{AIRPLANE_TYPE}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        airplane_type = create_and_return_airplane_type("test")
        url = reverse(f"airport:{AIRPLANE_TYPE}-detail", kwargs={"pk": airplane_type.pk})
        response = self.client.get(url)
        self.assertEqual(response.json(), AirplaneTypeDetailSerializer(airplane_type).data)

    def test_destroy(self):
        airplane_type = create_and_return_airplane_type("test")
        url = reverse(f"airport:{AIRPLANE_TYPE}-detail", kwargs={"pk": airplane_type.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        airplane_type = create_and_return_airplane_type("test")
        url = reverse(f"airport:{AIRPLANE_TYPE}-detail", kwargs={"pk": airplane_type.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)


class TestAirplaneTypeAuth(APITestCase):
    def setUp(self):
        user = create_and_return_user()
        self.client.force_authenticate(user)

    def test_post(self):
        data = {"name": "test"}
        url = reverse(f"airport:{AIRPLANE_TYPE}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AirplaneType.objects.count(), 1)
        self.assertEqual(AirplaneType.objects.first().name, "test")

    def test_destroy(self):
        airplane_type = create_and_return_airplane_type("test")
        url = reverse(f"airport:{AIRPLANE_TYPE}-detail", kwargs={"pk": airplane_type.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(AirplaneType.objects.count(), 0)

    def test_update(self):
        airplane_type = create_and_return_airplane_type("test")
        data = {"name": "test2"}
        url = reverse(f"airport:{AIRPLANE_TYPE}-detail", kwargs={"pk": airplane_type.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AirplaneType.objects.get(pk=airplane_type.pk).name, "test2")


class TestAirplane(APITestCase):
    def test_list(self):
        create_and_return_airplane("test1", "test2")
        create_and_return_airplane("test2", "test1")
        create_and_return_airplane("test3", "test3")
        url = reverse(f"airport:{AIRPLANE}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        airplane = create_and_return_airplane("test1", "test2")
        url = reverse(f"airport:{AIRPLANE}-detail", kwargs={"pk": airplane.pk})
        request = self.client.get(url)

        serializer = AirplaneRetrieveSerializer(airplane, context={'request': request.wsgi_request})
        self.assertEqual(request.json(), serializer.data)

    def test_destroy(self):
        airplane = create_and_return_airplane("test1", "test2")
        url = reverse(f"airport:{AIRPLANE}-detail", kwargs={"pk": airplane.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        airplane = create_and_return_airplane("test1", "test2")
        url = reverse(f"airport:{AIRPLANE}-detail", kwargs={"pk": airplane.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)


class TestAirplaneAuth(APITestCase):
    def setUp(self):
        user = create_and_return_user()
        self.client.force_authenticate(user)

    def test_post(self):
        data = {
            "airplane_type": create_and_return_airplane_type("test").id,
            "name": "test",
            "rows": 2,
            "seats_per_row": 4
        }
        url = reverse(f"airport:{AIRPLANE}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Airplane.objects.count(), 1)
        self.assertEqual(Airplane.objects.first().name, "test")

    def test_unique_airplane_constraint_create(self):
        data = {
            "airplane_type": create_and_return_airplane_type("test").id,
            "name": "test",
            "rows": 2,
            "seats_per_row": 4
        }
        url = reverse(f"airport:{AIRPLANE}-list")
        self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_destroy(self):
        airplane = create_and_return_airplane("test1", "test2")
        url = reverse(f"airport:{AIRPLANE}-detail", kwargs={"pk": airplane.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Airplane.objects.count(), 0)

    def test_update(self):
        airplane = create_and_return_airplane("test1", "test2")
        data = {"name": "test2"}
        url = reverse(f"airport:{AIRPLANE}-detail", kwargs={"pk": airplane.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Airplane.objects.get(pk=airplane.pk).name, "test2")


class TestAirport(APITestCase):
    def test_list(self):
        create_and_return_airport("test1", "test1", "test1")
        create_and_return_airport("test2", "test2", "test2")
        create_and_return_airport("test3", "test3", "test3")
        url = reverse(f"airport:{AIRPORT}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        airport = create_and_return_airport("test1", "test1", "test1")
        url = reverse(f"airport:{AIRPORT}-detail", kwargs={"pk": airport.pk})
        request = self.client.get(url)

        serializer = AirportDetailSerializer(airport, context={'request': request.wsgi_request})
        self.assertEqual(request.json(), serializer.data)

    def test_create(self):
        url = reverse(f"airport:{AIRPORT}-list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_destroy(self):
        airport = create_and_return_airport("test1", "test1", "test1")
        url = reverse(f"airport:{AIRPORT}-detail", kwargs={"pk": airport.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        airport = create_and_return_airport("test1", "test1", "test1")
        url = reverse(f"airport:{AIRPORT}-detail", kwargs={"pk": airport.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)


class TestAirportAuth(APITestCase):
    def setUp(self):
        user = create_and_return_user()
        self.client.force_authenticate(user)

    def test_post(self):
        data = {
            "name": "test",
            "closest_big_city": create_and_return_city("test", "test").id,
        }

        url = reverse(f"airport:{AIRPORT}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Airport.objects.count(), 1)
        self.assertEqual(Airport.objects.first().name, "test")

    def test_destroy(self):
        airport = create_and_return_airport("test1", "test1", "test1")
        url = reverse(f"airport:{AIRPORT}-detail", kwargs={"pk": airport.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Airport.objects.count(), 0)

    def test_update(self):
        airport = create_and_return_airport("test1", "test1", "test1")
        data = {"name": "test2"}
        url = reverse(f"airport:{AIRPORT}-detail", kwargs={"pk": airport.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Airport.objects.get(pk=airport.pk).name, "test2")


class TestRoute(APITestCase):
    def test_list(self):
        create_and_return_route(
            ["test", "test", "test"],
            ["test1", "test1", "test1"]
        )
        create_and_return_route(
            ["test2", "test2", "test2"],
            ["test3", "test3", "test3"]
        )
        create_and_return_route(
            ["test4", "test4", "test4"],
            ["test5", "test5", "test5"]
        )
        url = reverse(f"airport:{ROUTE}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        route = create_and_return_route(
            ["test", "test", "test"],
            ["test1", "test1", "test1"]
        )
        url = reverse(f"airport:{ROUTE}-detail", kwargs={"pk": route.pk})
        request = self.client.get(url)

        serializer = RouteWithSlugSerializer(
            route,
            context={'request': request.wsgi_request}
        )
        self.assertEqual(request.json(), serializer.data)

    def test_destroy(self):
        route = create_and_return_route(
            ["test", "test", "test"],
            ["test1", "test1", "test1"]
        )
        url = reverse(f"airport:{ROUTE}-detail", kwargs={"pk": route.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        route = create_and_return_route(
            ["test", "test", "test"],
            ["test1", "test1", "test1"]
        )
        url = reverse(f"airport:{ROUTE}-detail", kwargs={"pk": route.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)


class TestRouteAuth(APITestCase):
    def setUp(self):
        user = create_and_return_user()
        self.client.force_authenticate(user)

    def test_create(self):
        data = {
            "source": create_and_return_airport("test", "test", "test").pk,
            "destination": create_and_return_airport("test1", "test1", "test1").pk,
            "distance": 123
        }
        url = reverse(f"airport:{ROUTE}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Route.objects.count(), 1)

    def test_unique_route_constraint(self):
        route = create_and_return_route(
            ["test", "test", "test"],
            ["test1", "test1", "test1"]
        )
        data = {
            "source": route.source.pk,
            "destination": route.destination.pk,
            "distance": 12
        }
        url = reverse(f"airport:{ROUTE}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_destroy(self):
        route = create_and_return_route(
            ["test", "test", "test"],
            ["test1", "test1", "test1"]
        )
        url = reverse(f"airport:{ROUTE}-detail", kwargs={"pk": route.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        route = create_and_return_route(
            ["test", "test", "test"],
            ["test1", "test1", "test1"]
        )

        data = {
            "source": create_and_return_airport("test2", "test2", "test2").pk,
        }
        url = reverse(f"airport:{ROUTE}-detail", kwargs={"pk": route.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Route.objects.get(pk=route.pk).source.name, "test2")


class TestCrew(APITestCase):
    def test_list(self):
        create_and_return_crew("test", "test")
        create_and_return_crew("test1", "test1")
        create_and_return_crew("test2", "test2")
        url = reverse(f"airport:{CREW}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        crew = create_and_return_crew("test", "test")
        url = reverse(f"airport:{CREW}-detail", kwargs={"pk": crew.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_destroy(self):
        crew = create_and_return_crew("test", "test")
        url = reverse(f"airport:{CREW}-detail", kwargs={"pk": crew.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_create(self):
        url = reverse(f"airport:{CREW}-list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        crew = create_and_return_crew("test", "test")
        url = reverse(f"airport:{CREW}-detail", kwargs={"pk": crew.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 401)


class TestCrewAuth(APITestCase):
    def setUp(self):
        user = create_and_return_user()
        self.client.force_authenticate(user)

    def test_create(self):
        data = {
            "first_name": "test",
            "last_name": "test"
        }
        url = reverse(f"airport:{CREW}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Crew.objects.count(), 1)

    def test_destroy(self):
        crew = create_and_return_crew("test", "test")
        url = reverse(f"airport:{CREW}-detail", kwargs={"pk": crew.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        crew = create_and_return_crew("test", "test")
        data = {"first_name": "test1"}
        url = reverse(f"airport:{CREW}-detail", kwargs={"pk": crew.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Crew.objects.get(pk=crew.pk).first_name, "test1")


class TestFlight(APITestCase):
    def setUp(self):
        self.flight = create_and_return_flight(
            ["first_name", "last_name"],
            [
                ["source_airport_name", "source_city_name", "source_country_name"],
                ["destination_airport_name", "destination_city_name", "destination_country_name"]
            ],
            ["airplane_name", "airplane_type_name"]

        )

    def test_list(self):
        url = reverse(f"airport:{FLIGHT}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        url = reverse(f"airport:{FLIGHT}-detail", kwargs={"pk": self.flight.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_tickets_actions(self):
        Ticket.objects.create(
            flight=self.flight,
            row=1,
            seat=1,
            order=Order.objects.create()
        )
        url = reverse(f"airport:{FLIGHT}-tickets", kwargs={"pk": self.flight.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_destroy(self):
        url = reverse(f"airport:{FLIGHT}-detail", kwargs={"pk": self.flight.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_create(self):
        url = reverse(f"airport:{FLIGHT}-list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        url = reverse(f"airport:{FLIGHT}-detail", kwargs={"pk": self.flight.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 401)


class TestFlightAuth(APITestCase):
    def setUp(self):
        user = create_and_return_user()
        self.client.force_authenticate(user)

    def test_create(self):
        data = {
            "crew": [create_and_return_crew("test", "test").pk],
            "route": create_and_return_route(
                ["source_airport_name", "source_city_name", "source_country_name"],
                ["destination_airport_name", "destination_city_name", "destination_country_name"]
            ).pk,
            "airplane": create_and_return_airplane(
                "airplane_name", "airplane_type_name"
            ).pk,
            "departure_time": "2021-01-01T00:00:00Z",
            "arrival_time": "2021-01-01T00:00:00Z",
        }
        url = reverse(f"airport:{FLIGHT}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_destroy(self):
        flight = create_and_return_flight(
            ["first_name", "last_name"],
            [
                ["source_airport_name", "source_city_name", "source_country_name"],
                ["destination_airport_name", "destination_city_name", "destination_country_name"]
            ],
            ["airplane_name", "airplane_type_name"]
        )
        url = reverse(f"airport:{FLIGHT}-detail", kwargs={"pk": flight.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        flight = create_and_return_flight(
            ["first_name", "last_name"],
            [
                ["source_airport_name", "source_city_name", "source_country_name"],
                ["destination_airport_name", "destination_city_name", "destination_country_name"]
            ],
            ["airplane_name", "airplane_type_name"]
        )
        url = reverse(f"airport:{FLIGHT}-detail", kwargs={"pk": flight.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 200)


class TestOrder(APITestCase):
    def test_list(self):
        url = reverse(f"airport:{ORDER}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_detail(self):
        order = create_and_return_order(create_and_return_user())
        url = reverse(f"airport:{ORDER}-detail", kwargs={"pk": order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_create(self):
        url = reverse(f"airport:{ORDER}-list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_destroy(self):
        order = create_and_return_order(create_and_return_user())
        url = reverse(f"airport:{ORDER}-detail", kwargs={"pk": order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        order = create_and_return_order(create_and_return_user())
        url = reverse(f"airport:{ORDER}-detail", kwargs={"pk": order.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 401)


class TestOrderUserAuth(APITestCase):
    def setUp(self):
        self.user = create_and_return_user(is_staff=False)
        self.client.force_authenticate(self.user)
        for _ in range(3):
            create_and_return_order(self.user)

    def test_list(self):
        url = reverse(f"airport:{ORDER}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_list_other_user(self):
        other_user = create_and_return_user(
            username="other_user",
            email="other_user@example.com",
            is_staff=False
        )
        self.client.force_authenticate(other_user)
        url = reverse(f"airport:{ORDER}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_detail(self):
        order = create_and_return_order(self.user)
        url = reverse(f"airport:{ORDER}-detail", kwargs={"pk": order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_detail(self):
        user = create_and_return_user(
            username="other_user",
            email="other_user@example.com",
        )
        order = create_and_return_order(user)
        url = reverse(f"airport:{ORDER}-detail", kwargs={"pk": order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        url = reverse(f"airport:{ORDER}-list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.get(id=response.data["id"]).user, self.user)

    def test_delete(self):
        order = create_and_return_order(self.user)
        url = reverse(f"airport:{ORDER}-detail", kwargs={"pk": order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_update(self):
        order = create_and_return_order(self.user)
        url = reverse(f"airport:{ORDER}-detail", kwargs={"pk": order.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 403)


class TestOrderStaffAuth(APITestCase):
    def setUp(self):
        self.user = create_and_return_user()
        self.client.force_authenticate(self.user)

        user = create_and_return_user(
            username="other_user",
            email="other_user@example.com",
            is_staff=False
        )
        for _ in range(3):
            create_and_return_order(user)

    def test_list(self):
        url = reverse(f"airport:{ORDER}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_detail(self):
        order = create_and_return_order(self.user)
        url = reverse(f"airport:{ORDER}-detail", kwargs={"pk": order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_destroy(self):
        order = create_and_return_order(self.user)
        url = reverse(f"airport:{ORDER}-detail", kwargs={"pk": order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class TestTicket(APITestCase):
    def test_list(self):
        url = reverse(f"airport:{TICKET}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_detail(self):
        user = create_and_return_user()
        ticket = create_and_return_ticket(
            user=user,
            flight=[
                ["first_name", "last_name"],
                [
                    ["source_airport_name", "source_city_name", "source_country_name"],
                    ["destination_airport_name", "destination_city_name", "destination_country_name"],
                ],
                ["airplane_name", "airplane_type_name"]
            ]
        )
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": ticket.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_destroy(self):
        user = create_and_return_user()
        ticket = create_and_return_ticket(
            user=user,
            flight=[
                ["first_name", "last_name"],
                [
                    ["source_airport_name", "source_city_name", "source_country_name"],
                    ["destination_airport_name", "destination_city_name", "destination_country_name"],
                ],
                ["airplane_name", "airplane_type_name"]
            ]
        )
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": ticket.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        user = create_and_return_user()
        ticket = create_and_return_ticket(
            user=user,
            flight=[
                ["first_name", "last_name"],
                [
                    ["source_airport_name", "source_city_name", "source_country_name"],
                    ["destination_airport_name", "destination_city_name", "destination_country_name"],
                ],
                ["airplane_name", "airplane_type_name"]
            ]
        )
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": ticket.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)

    def test_create(self):
        url = reverse(f"airport:{TICKET}-list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)


class TestTicketStaffAuth(APITestCase):
    def setUp(self):
        self.user = create_and_return_user()
        self.client.force_authenticate(self.user)

        user = create_and_return_user(
            username="other_user",
            email="other_user@example.com",
            is_staff=False
        )
        self.ticket = create_and_return_ticket(
            user=user,
            flight=[
                ["first_name", "last_name"],
                [
                    ["source_airport_name", "source_city_name", "source_country_name"],
                    ["destination_airport_name", "destination_city_name", "destination_country_name"],
                ],
                ["airplane_name", "airplane_type_name"]
            ]
        )

    def test_list(self):
        url = reverse(f"airport:{TICKET}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_detail(self):
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": self.ticket.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        data = {
            "order": create_and_return_order(self.user).pk,
            "flight": self.ticket.flight.pk,
            "row": 1,
            "seat": 2
        }
        url = reverse(f"airport:{TICKET}-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_unique_ticket_constraint(self):
        data = {
            "order": create_and_return_order(self.user).pk,
            "flight": self.ticket.flight.pk,
            "row": 1,
            "seat": 2
        }
        url = reverse(f"airport:{TICKET}-list")
        self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_destroy(self):
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": self.ticket.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": self.ticket.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 200)


class TestTicketUserAuth(APITestCase):
    def setUp(self):
        self.user = create_and_return_user(is_staff=False)
        self.client.force_authenticate(self.user)
        self.ticket = create_and_return_ticket(
            user=self.user,
            flight=[
                ["first_name1", "last_name1"],
                [
                    ["source_airport_name1", "source_city_name1", "source_country_name1"],
                    ["destination_airport_name1", "destination_city_name1", "destination_country_name1"],
                ],
                ["airplane_name1", "airplane_type_name1"]
            ]
        )

        user = create_and_return_user(
            username="test1",
            email="test1@example.com",
        )
        self.other_ticket = create_and_return_ticket(
            user=user,
            flight=[
                ["first_name", "last_name"],
                [
                    ["source_airport_name", "source_city_name", "source_country_name"],
                    ["destination_airport_name", "destination_city_name", "destination_country_name"],
                ],
                ["airplane_name", "airplane_type_name"]
            ]
        )

    def test_list(self):
        url = reverse(f"airport:{TICKET}-list")
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)

    def test_invalid_detail(self):
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": self.other_ticket.pk})
        request = self.client.get(url)
        self.assertEqual(request.status_code, 404)

    def test_detail(self):
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": self.ticket.pk})
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)

    def test_destroy(self):
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": self.ticket.pk})
        request = self.client.delete(url)
        self.assertEqual(request.status_code, 403)

    def test_update(self):
        url = reverse(f"airport:{TICKET}-detail", kwargs={"pk": self.ticket.pk})
        request = self.client.patch(url)
        self.assertEqual(request.status_code, 403)

    def test_create(self):
        data = {
            "order": create_and_return_order(self.user).pk,
            "flight": self.ticket.flight.pk,
            "row": 2,
            "seat": 2
        }
        url = reverse(f"airport:{TICKET}-list")
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

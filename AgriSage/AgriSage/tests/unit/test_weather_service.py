from backend.services.weather_service import INDIA_CENTROID, resolve_coordinates


def test_device_coordinates_take_precedence_over_state_fallback():
    assert resolve_coordinates(
        state="Rajasthan",
        district="Jaipur",
        lat=26.9124,
        lon=75.7873,
    ) == (26.9124, 75.7873)


def test_state_fallback_is_not_kerala_for_india_wide_requests():
    latitude, longitude = resolve_coordinates(state="Rajasthan")

    assert (latitude, longitude) != (9.9816, 76.2999)
    assert latitude > 20
    assert longitude < 80


def test_unknown_state_uses_india_centroid():
    assert resolve_coordinates(state="Unknown state") == INDIA_CENTROID


def test_known_kerala_district_remains_supported():
    latitude, longitude = resolve_coordinates(state="Kerala", district="Ernakulam")

    assert round(latitude, 4) == 9.9816
    assert round(longitude, 4) == 76.2999

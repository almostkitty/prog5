import getweatherdata
import pytest
import os


key = os.getenv('owm_api_key', '')

def test_without_key():
    assert getweatherdata.get_weather_data("Moscow", api_key=None) is None

def test_in_riga():
    assert getweatherdata.get_weather_data("Riga", api_key=key) is not None

def test_type_of_res():
    assert isinstance(getweatherdata.get_weather_data("Riga", api_key=key), dict)

def test_args_error():
    assert getweatherdata.get_weather_data('', api_key=key) is None

def test_pos_arg_error():
    assert getweatherdata.get_weather_data('', api_key=key) is None

def test_coords_dim():
    data = getweatherdata.get_weather_data('Riga', api_key=key)
    assert data is not None and len(data.get('coord')) == 2

def test_temp_type():
    data = getweatherdata.get_weather_data('Riga', api_key=key)
    assert data is not None and isinstance(data.get('feels_like'), float)

inp_params_countries = [
    ("Chicago", key, 'US'),
    ("Saint Petersburg", key, 'RU'),
    ("Dhaka", key, 'BD'),
    ("Minsk", key, 'BY'),
    ("Kyoto", key, 'JP'),
    ("Anchorage", key, 'US'),
    ("Havana", key, 'CU')
]

@pytest.mark.parametrize("city, api_key, expected_country", inp_params_countries)
def test_countries(city, api_key, expected_country):
    data = getweatherdata.get_weather_data(city, api_key=key)
    assert data is not None and data.get('country', 'NoValue') == expected_country

inp_params_timezones = [
    ("Chicago", key, 'UTC-5'),
    ("Saint Petersburg", key, 'UTC+3'),
    ("Dhaka", key, 'UTC+6'),
    ("Minsk", key, 'UTC+3'),
    ("Kyoto", key, 'UTC+9'),
    ("Anchorage", key, 'UTC-8'),
    ("Havana", key, 'UTC-4')
]

@pytest.mark.parametrize("city, api_key, expected_time", inp_params_timezones)
def test_utc_time(city, api_key, expected_time):
    data = getweatherdata.get_weather_data(city, api_key=key)
    assert data is not None and data.get('timezone', 'NoValue') == expected_time

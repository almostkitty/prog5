import pytest
from unittest.mock import patch, Mock
from main import CurrenciesList, DecoratorJSON, DecoratorCSV


# Тест для CurrenciesList
@patch('main.requests.get')
def test_currencies_list(mock_get):
    """Тестирование получения данных с сайта ЦБ"""

    # Создаём мок-ответ
    mock_response = Mock()
    mock_response.content = """
    <ValCurs Date="11.01.2025" name="Foreign Currency Market">
        <Valute ID="R01020A">
            <NumCode>944</NumCode>
            <CharCode>AZN</CharCode>
            <Name>Азербайджанский манат</Name>
            <Value>59,9498</Value>
            <VunitRate>59,9498</VunitRate>
        </Valute>
        <Valute ID="R01035">
            <NumCode>826</NumCode>
            <CharCode>GBP</CharCode>
            <Nominal>1</Nominal>
            <Name>Фунт стерлингов</Name>
            <Value>125,3855</Value>
            <VunitRate>125,3855</VunitRate>
        </Valute>
    </ValCurs>
    """

    mock_get.return_value = mock_response

    currencies_list = CurrenciesList()
    result = currencies_list.fetch()

    expected_result = {
        'AZN': {'name': 'Азербайджанский манат', 'value': 59.9498, 'nominal': 1},
        'GBP': {'name': 'Фунт стерлингов', 'value': 125.3855, 'nominal': 1}
    }


    assert result == expected_result, "Ошибка получения данных с сайта"


def test_decorator_json():
    """Тестирование декоратора JSON"""
    currencies_data = {
        'AZN': {'name': 'Азербайджанский манат', 'value': 59.9498},
        'GBP': {'name': 'Фунт стерлингов', 'value': 125.3855}
    }
    
    currencies_list = Mock()
    currencies_list.fetch.return_value = currencies_data

    json_decorator = DecoratorJSON(currencies_list)
    result = json_decorator.fetch()
    

    expected_result = """
{
  "AZN": {
    "name": "Азербайджанский манат",
    "value": 59.9498
  },
  "GBP": {
    "name": "Фунт стерлингов",
    "value": 125.3855
  }
}
"""
    assert result == expected_result.strip(), "Ошибка с декоратором json"


def test_decorator_csv():
    """Тестирование декоратора CSV"""
    currencies_data = {
        'AZN': {'name': 'Азербайджанский манат', 'value': 59.9498, 'nominal': 1},
        'GBP': {'name': 'Фунт стерлингов', 'value': 125.3855, 'nominal': 1}
    }

    currencies_list = Mock()
    currencies_list.fetch.return_value = currencies_data

    csv_decorator = DecoratorCSV(currencies_list)
    result = csv_decorator.fetch()
    result = result.replace('\r\n', '\n')

    expected_result = "CharCode,Name,Value,Nominal\nAZN,Азербайджанский манат,59.9498,1\nGBP,Фунт стерлингов,125.3855,1"
    
    # Чтобы отловить ошибку
    # print("Actual Result:", repr(result))
    # print("Expected Result:", repr(expected_result))

    assert result.strip() == expected_result, "Ошибка с декоратором csv"




def test_decorator_csv_exception():
    """Тестирование исключения при передаче строки в csv декоратор"""
    currencies_list = Mock()
    currencies_list.fetch.return_value = '{"AZN": {"name": "Азербайджанский манат", "value": 59.9498}}'  # Неправильный вариант

    csv_decorator = DecoratorCSV(currencies_list)
    with pytest.raises(TypeError, match="Не форматируется"):
        csv_decorator.fetch()

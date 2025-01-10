import pytest
from unittest.mock import patch, Mock
from main import CurrencyManager


@pytest.fixture
def currency_manager():
    """
    Создание экземпляра CurrencyManager для тестов для использования свежего экземпляра класса в каждом тесте
    """
    return CurrencyManager()


def test_set_and_get_min(currency_manager):
    """
    Тестирование установки и получения минимального интервала между запросами
    """
    currency_manager.set_min_interval(5)
    assert currency_manager.get_min_interval() == 5


@patch("main.requests.get")
def test_get_currencies(mock_get, currency_manager):
    """
    Тестирование метода get_currencies с использованием mock для запроса данных.
    Проверяем, что метод возвращает правильные значения для заданных ID валют.
    """

    # Создаём мокающий ответ, который эмулирует ответ от сервера
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

    # Подставляем этот ответ вместо реального HTTP-запроса
    mock_get.return_value = mock_response

    # Вызываем метод с тестовыми ID валют
    result = currency_manager.get_currencies(['R01020A', 'R01035'])

    # Ожидаемый результат на основе подставленного mock-ответа
    expected_result = [
        {'AZN': ('Азербайджанский манат', (59,9498))},
        {'GBP': ('Фунт стерлингов', (125,3855))}
    ]

    # Проверяем, что результат совпадает с ожидаемым
    assert result == expected_result


@patch("main.os.makedirs")
@patch("main.plt.savefig")
def test_visualize(mock_savefig, mock_makedirs, currency_manager):
    """
    Тестирование метода visualize_currencies.
    Проверяем, что графики сохраняются в правильную папку, 
    а необходимые действия (создание папки и сохранение файла) вызываются.
    """

    # Данные для визуализации
    currency_manager.currencies = [
        {'AZN': ('Азербайджанский манат', (59,9498))},
        {'GBP': ('Фунт стерлингов', (125,3855))}
    ]

    # Вызываем метод визуализации с тестовой папкой
    currency_manager.visualize_currencies(folder='test_graphs')

    # Проверяем что папка создана
    mock_makedirs.assert_called_once_with('test_graphs')

    # Проверяем что график сохранён
    mock_savefig.assert_called_once()


@patch("main.time.time", side_effect=[0, 0.5])  # Мокаем время сначала 0, затем 0.5
def test_too_frequent(mock_time, currency_manager):
    """Тестирование на частоту запросов"""
    currency_manager.set_min_interval(2)
    
    with pytest.raises(Exception, match="Запросы разрешено отправлять не чаще, чем каждые 2 секунд."):
        currency_manager.get_currencies(['R01020A'])

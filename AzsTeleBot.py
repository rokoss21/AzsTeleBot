import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from bs4 import BeautifulSoup

CITY_CHOICE, = range(1)

# Словарь городов и соответствующих URL
CITIES = {
    '1': ('Архангельск', 'https://azsprice.ru/arhangelsk'),
    '2': ('Астрахань', 'https://azsprice.ru/astrahan'),
    '3': ('Барнаул', 'https://azsprice.ru/barnaul'),
    '4': ('Белгород', 'https://azsprice.ru/belgorod'),
    '5': ('Благовещенск', 'https://azsprice.ru/blagoveschensk'),
    '6': ('Братск', 'https://azsprice.ru/bratsk'),
    '7': ('Брянск', 'https://azsprice.ru/bryansk'),
    '8': ('Владивосток', 'https://azsprice.ru/vladivostok'),
    '9': ('Владимир', 'https://azsprice.ru/vladimir'),
    '10': ('Волгоград', 'https://azsprice.ru/volgograd'),
    '11': ('Волжский', 'https://azsprice.ru/volzhskiy'),
    '12': ('Вологда', 'https://azsprice.ru/vologda'),
    '13': ('Воронеж', 'https://azsprice.ru/voronezh'),
    '14': ('Екатеринбург', 'https://azsprice.ru/ekaterinburg'),
    '15': ('Иваново', 'https://azsprice.ru/ivanovo'),
    '16': ('Ижевск', 'https://azsprice.ru/izhevsk'),
    '17': ('Иркутск', 'https://azsprice.ru/irkutsk'),
    '18': ('Казань', 'https://azsprice.ru/kazan'),
    '19': ('Калининград', 'https://azsprice.ru/kaliningrad'),
    '20': ('Калуга', 'https://azsprice.ru/kaluga'),
    '21': ('Кемерово', 'https://azsprice.ru/kemerovo'),
    '22': ('Киров', 'https://azsprice.ru/kirov'),
    '23': ('Комсомольск-на-Амуре', 'https://azsprice.ru/komsomolsk-na-amure'),
    '24': ('Кострома', 'https://azsprice.ru/kostroma'),
    '25': ('Краснодар', 'https://azsprice.ru/krasnodar'),
    '26': ('Красноярск', 'https://azsprice.ru/krasnoyarsk'),
    '27': ('Курган', 'https://azsprice.ru/kurgan'),
    '28': ('Курск', 'https://azsprice.ru/kursk'),
    '29': ('Липецк', 'https://azsprice.ru/lipeck'),
    '30': ('Магнитогорск', 'https://azsprice.ru/magnitogorsk'),
    '31': ('Москва', 'https://azsprice.ru/moskva'),
    '32': ('Мурманск', 'https://azsprice.ru/murmansk'),
    '33': ('Мытищи', 'https://azsprice.ru/mytischi'),
    '34': ('Набережные Челны', 'https://azsprice.ru/naberezhnye-chelny'),
    '35': ('Нальчик', 'https://azsprice.ru/nalchik'),
    '36': ('Нижнекамск', 'https://azsprice.ru/nizhnekamsk'),
    '37': ('Нижний Новгород', 'https://azsprice.ru/nizhniy-novgorod'),
    '38': ('Новокузнецк', 'https://azsprice.ru/novokuzneck'),
    '39': ('Новочеркасск', 'https://azsprice.ru/novocherkassk'),
    '40': ('Новосибирск', 'https://azsprice.ru/novosibirsk'),
    '41': ('Одинцово', 'https://azsprice.ru/odincovo'),
    '42': ('Омск', 'https://azsprice.ru/omsk'),
    '43': ('Орел', 'https://azsprice.ru/orel'),
    '44': ('Оренбург', 'https://azsprice.ru/orenburg'),
    '45': ('Орск', 'https://azsprice.ru/orsk'),
    '46': ('Пенза', 'https://azsprice.ru/penza'),
    '47': ('Пермь', 'https://azsprice.ru/perm'),
    '48': ('Петрозаводск', 'https://azsprice.ru/petrozavodsk'),
    '49': ('Псков', 'https://azsprice.ru/pskov'),
    '50': ('Ростов-на-Дону', 'https://azsprice.ru/rostov-na-donu'),
    '51': ('Рязань', 'https://azsprice.ru/ryazan'),
    '52': ('Самара', 'https://azsprice.ru/samara'),
    '53': ('Санкт-Петербург', 'https://azsprice.ru/sankt-peterburg'),
    '54': ('Саранск', 'https://azsprice.ru/saransk'),
    '55': ('Саратов', 'https://azsprice.ru/saratov'),
    '56': ('Симферополь', 'https://azsprice.ru/simferopol'),
    '57': ('Смоленск', 'https://azsprice.ru/smolensk'),
    '58': ('Сочи', 'https://azsprice.ru/sochi'),
    '59': ('Ставрополь', 'https://azsprice.ru/stavropol'),
    '60': ('Старый Оскол', 'https://azsprice.ru/stariy-oskol'),
    '61': ('Стерлитамак', 'https://azsprice.ru/sterlitamak'),
    '62': ('Сургут', 'https://azsprice.ru/surgut'),
    '63': ('Сыктывкар', 'https://azsprice.ru/syktyvkar'),
    '64': ('Тамбов', 'https://azsprice.ru/tambov'),
    '65': ('Тверь', 'https://azsprice.ru/tver'),
    '66': ('Тольятти', 'https://azsprice.ru/tolyatti'),
    '67': ('Томск', 'https://azsprice.ru/tomsk'),
    '68': ('Тула', 'https://azsprice.ru/tula'),
    '69': ('Тюмень', 'https://azsprice.ru/tyumen'),
    '70': ('Ульяновск', 'https://azsprice.ru/ulyanovsk'),
    '71': ('Улан-Удэ', 'https://azsprice.ru/ulan-ude'),
    '72': ('Уфа', 'https://azsprice.ru/ufa'),
    '73': ('Хабаровск', 'https://azsprice.ru/habarovsk'),
    '74': ('Чебоксары', 'https://azsprice.ru/cheboksary'),
    '75': ('Челябинск', 'https://azsprice.ru/chelyabinsk'),
    '76': ('Чита', 'https://azsprice.ru/chita'),
    '77': ('Шахты', 'https://azsprice.ru/shahty'),
    '78': ('Щекино', 'https://azsprice.ru/schekino'),
    '79': ('Энгельс', 'https://azsprice.ru/engels'),
    '80': ('Ярославль', 'https://azsprice.ru/yaroslavl'),
    '81': ('Йошкар-Ола', 'https://azsprice.ru/yoshkar-ola')


    # Добавьте другие города по аналогии
}

# Функция для получения HTML-кода страницы
def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, что запрос успешен
        return response.text
    except requests.RequestException as e:
        return None

# Функция для парсинга данных со страницы
def parse_azs_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    azs_cards = soup.find_all('div', class_='card')
    azs_data = []

    for card in azs_cards:
        name_header = card.find('h4')
        name = name_header.text.strip() if name_header else "Неизвестное название"

        brand_info = card.find('small', class_='text-muted')
        brand = brand_info.text.strip() if brand_info else "Неизвестный бренд"

        address_info = card.find('p', class_='card-title')
        address = address_info.text.strip() if address_info else "Неизвестный адрес"

        fuel_info_list = card.find_all('li')
        for fuel_info in fuel_info_list:
            text = fuel_info.get_text(strip=True)
            parts = text.split(':')
            if len(parts) >= 2:
                fuel_type = parts[0].strip()
                price_and_date_text = parts[1].strip().split('₽')
                price_text = price_and_date_text[0].strip()
                date = price_and_date_text[1].strip() if len(price_and_date_text) > 1 else None
                try:
                    price = float(price_text)
                    azs_data.append({
                        'name': name,
                        'brand': brand,
                        'address': address,
                        'fuel_type': fuel_type,
                        'price': price,
                        'date': date
                    })
                except ValueError:
                    continue  # Пропускаем неверные записи
                    
    return azs_data

# Функция для нахождения минимальной цены для каждого типа топлива
def find_min_prices(azs_data):
    min_prices = {}
    for entry in azs_data:
        fuel_type = entry['fuel_type']
        if fuel_type not in min_prices or entry['price'] < min_prices[fuel_type]['price']:
            min_prices[fuel_type] = entry
    return min_prices

def start(update: Update, context: CallbackContext) -> int:
    reply_text = "Выберите город, отправив его номер:\n" + "\n".join([f"{num}. {info[0]}" for num, info in CITIES.items()])
    update.message.reply_text(reply_text)
    return CITY_CHOICE

def city_choice(update: Update, context: CallbackContext) -> int:
    chosen_number = update.message.text
    if chosen_number in CITIES:
        context.user_data['city_url'] = CITIES[chosen_number][1]  # URL
        update.message.reply_text(f"Город выбран: {CITIES[chosen_number][0]}. Используйте команду /fuel для получения информации о ценах на топливо.")
        return ConversationHandler.END
    else:
        update.message.reply_text("Пожалуйста, выберите номер из списка.")
        return CITY_CHOICE

def fuel(update: Update, context: CallbackContext) -> None:
    city_url = context.user_data.get('city_url')
    if not city_url:
        update.message.reply_text("Сначала выберите город командой /start.")
        return
    
    html = get_html(city_url)
    if html:
        azs_data = parse_azs_data(html)
        min_prices = find_min_prices(azs_data)
        for fuel, info in min_prices.items():
            update.message.reply_text(
                f"{fuel}: {info['price']} рублей\n"
                f"Заправка: {info['brand']}\n"
                f"Адрес: {info['address']}\n"
                f"Дата: {info['date']}\n"
            )

def start_bot():
    TOKEN = "6477019130:AAHXaXx0EVcYV2EhajhtTxOZCZapqan5Mtc"
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={CITY_CHOICE: [MessageHandler(Filters.text & ~Filters.command, city_choice)]},
        fallbacks=[]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("fuel", fuel))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    start_bot()

Этот Telegram-бот позволяет создавать и распознавать QR-коды. Вы можете отправить текст для создания QR-кода или отправить изображение с QR-кодом для его распознавания.

## Функции

- **Создание QR-кода**: Отправьте текст, и бот сгенерирует для вас QR-код.
- **Распознавание QR-кода**: Отправьте изображение с QR-кодом, и бот распознает его содержимое.


## Живая демонстрация

### Посмотреть бота можно - [тут](https://t.me/qr_generate_jamalskiy_bot)

## Структура бота

<pre><code>
qr_generate_bot/
│
├── config/
│   └── config.py          # Конфигурации (API Token)
│
├── handlers/
│   └── qr_handlers.py     # Логика обработки запросов (создание и распознавание QR-кодов)
│
├── main.py                # Основной файл для запуска бота
│
├── requirements.txt       # Список зависимостей
│
└── gif.mp4                # Видео для /start
</code></pre>

## Установка

### 1. Клонируйте репозиторий

<pre><code>git clone https://github.com/jamalskiy/qr_generate_bot.git</code></pre>

### 2. Перейдите в папку с ботом

<pre><code>cd qr-code-bot</code></pre>

### 3. Установите нужные завимости

<pre><code>pip install -r requirements.txt</code></pre>

### 4. Вставьте токен бота в конфиг

<pre><code>nano config/config.py</code></pre>

### 5. Запустите бота

<pre><code>python3 main.py</code></pre>

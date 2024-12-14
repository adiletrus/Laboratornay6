from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, request, jsonify
import nltk

# Загрузка необходимых данных для nltk
nltk.download('stopwords') #список стоп-слов например, "the", "is", "and"
nltk.download('punkt') #разделения текста на предложения и слова
from nltk.corpus import stopwords

# Настройка стоп-слов
stop_words = set(stopwords.words('english'))

# Инициализация модели анализа тональности
sentiment_pipeline = pipeline("sentiment-analysis")

# Функция для извлечения ключевых слов
def extract_keywords(text, n_keywords=5):
    vectorizer = CountVectorizer(max_features=1000, stop_words='english')
    vectorizer.fit([text])
    keywords = vectorizer.get_feature_names_out()
    return list(keywords[:n_keywords])

# Создание Flask-приложения
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        # Получение данных из POST-запроса
        data = request.json
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'Text is required'}), 400

        # Анализ тональности текста
        sentiment = sentiment_pipeline(text)

        # Извлечение ключевых слов
        keywords = extract_keywords(text)

        # Формирование ответа
        return jsonify({
            'sentiment': sentiment,
            'keywords': keywords
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)

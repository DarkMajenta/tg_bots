import requests
import random

def get_video_comments(video_url):
    # Получение HTML-страницы с комментариями видео
    response = requests.get(video_url)
    html = response.text
    
    # Парсинг комментариев из HTML
    comments = []
    start_index = html.find('comment-renderer-text-content')
    while start_index != -1:
        start_index = html.find('>', start_index + 1)
        end_index = html.find('</', start_index)
        comment = html[start_index + 1 : end_index].strip()
        comments.append(comment)
        start_index = html.find('comment-renderer-text-content', end_index)
    
    return comments

def choose_random_winner(comments):
    # Выбор случайного победителя из списка комментариев
    winner = random.choice(comments)
    return winner

# Пример использования
video_url = "https://www.youtube.com/watch?v=VIDEO_ID"  # Замените VIDEO_ID на фактический идентификатор видео
comments = get_video_comments(video_url)
winner = choose_random_winner(comments)

print("Список комментариев:")
for comment in comments:
    print(comment)
    
print("\nПобедитель:")
print(winner)

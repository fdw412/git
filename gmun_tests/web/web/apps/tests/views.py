from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Article, Comment
import json, requests, random
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'tests/list.html', {'latest_articles_list':latest_articles_list})

@csrf_exempt
def buttons(request):
    pass

@csrf_exempt
def callserv(request):
    # return HttpResponse("25a8fedb")
    access_token = "9d26861b7c600e7aa1a8f5f64d9cf167e360d7a3744a188e6c63aff86facfddeb45ac0032f8135fa4b5ec"
    try:
        data = json.loads(request.body.decode())
        print(f"data     {data}")
        if str(data['type']) == "message_event":
            event_id = data['object']['event_id']
            button_number = int(data['object']['payload']['button'])
            conversation_message_id = data['object']['conversation_message_id']
            print(f"data =======   {data}\nevent_id =======   {event_id}\nbutton number =======  {button_number}\nconversation_message_id ==============   {conversation_message_id}")

            def send_event(event_data, event_id = event_id):
                url = "https://api.vk.com/method/messages.sendMessageEventAnswer?user_id=585675&v=5.120&"+\
                      f"access_token={access_token}" \
                      "&peer_id=585675&"+f"{event_data}"+"&event_id=" + f"{event_id}"
                print("url =======", url)
                response = requests.request("GET", url)
                print("=========send============", response.text.encode('utf8'))

            def send_msg(text):
                url = f"https://api.vk.com/method/messages.send?group_id=156180931&user_id=585675&v=5.107&access_token=" \
                      f"{access_token}&message={text}&dont_parse_links=1&random_id={random.randint(1, 99999)}"
                response = requests.request("GET", url)
                print("=========send_msg============", response.text.encode('utf8'))

            if button_number == 1:
                event_data = "event_data={  \"type\": \"open_app\",  \"app_id\": 5728966,  \"owner_id\": 156180931,  \"hash\": \"string\"}"
                print("event_data =======", event_data)
                send_event(event_data)

            if button_number == 2:
                event_data = "event_data={\"type\": \"show_snackbar\",\"text\": \" \"}"
                print("event_data =======", event_data)
                send_event(event_data)

            if button_number == 3:
                event_data = "event_data={\"type\": \"open_link\",\"link\": \"https://www.ikea.com/ru/ru/customer-service/contact-us/\"}"
                print("event_data =======", event_data)
                send_event(event_data)

            keyboard4 = {
                "inline": True,
                "buttons": [
                    [
                        {
                            "action": {
                                "type": "callback",
                                "payload": "{\"button\": \"1\"}",
                                "label": "Посмотреть каталог"
                            }
                        }
                    ],
                    [
                        {
                            "action": {
                                "type": "callback",
                                "payload": "{\"button\": \"2\"}",
                                "label": "Обсудить детали заказа"
                            }
                        }
                    ],
                    [
                        {
                            "action": {
                                "type": "callback",
                                "payload": "{\"button\": \"3\"}",
                                "label": "Контакты"
                            }
                        }
                    ],
                    [
                        {
                            "action": {
                                "type": "callback",
                                "payload": "{\"button\": \"4\"}",
                                "label": "В консервы"
                            }
                        }
                    ]
                ]
            }
            keyboard4 = json.dumps(keyboard4, ensure_ascii=False).encode('utf-8')
            keyboard4 = str(keyboard4.decode('utf-8'))

            keyboard5 = {
                "inline": True,
                "buttons": [
                    [
                        {
                            "action": {
                                "type": "callback",
                                "payload": "{\"button\": \"1\"}",
                                "label": "Посмотреть каталог"
                            }
                        }
                    ],
                    [
                        {
                            "action": {
                                "type": "callback",
                                "payload": "{\"button\": \"2\"}",
                                "label": "Обсудить детали заказа"
                            }
                        }
                    ],
                    [
                        {
                            "action": {
                                "type": "callback",
                                "payload": "{\"button\": \"3\"}",
                                "label": "Контакты"
                            }
                        }
                    ],
                    [
                        {
                            "action": {
                                "type": "callback",
                                "payload": "{\"button\": \"5\"}",
                                "label": "В пирожные"
                            }
                        }
                    ]
                ]
            }
            keyboard5 = json.dumps(keyboard5, ensure_ascii=False).encode('utf-8')
            keyboard5 = str(keyboard5.decode('utf-8'))



            if button_number == 4:
                event_data = "event_data={\"type\": \"show_snackbar\",\"text\": \"555555555555555555\"}"
                print("event_data =======", event_data)
                send_event(event_data)

                message = "КОНСЕРВЫ - ЭТО СИЛА"
                url = f"https://api.vk.com/method/messages.edit?group_id=196990463&v=5.85&access_token={access_token}&message={message}&peer_id=585675&conversation_message_id={conversation_message_id}&keyboard={keyboard5}"
                print(f"url     {url}")
                headers = {'Content-Type': 'application/json'}
                response = requests.request("GET", url, headers=headers)
                print(response.text)

            if button_number == 5:
                event_data = "event_data={\"type\": \"show_snackbar\",\"text\": \"111111111111111111\"}"
                print("event_data =======", event_data)
                send_event(event_data)

                message = "ПИРОЖНЫЕ - ЭТО КРАСИВО"
                url = f"https://api.vk.com/method/messages.edit?group_id=196990463&v=5.85&access_token={access_token}&message={message}&peer_id=585675&conversation_message_id={conversation_message_id}&keyboard={keyboard4}"
                print(f"url     {url}")
                headers = {'Content-Type': 'application/json'}
                response = requests.request("GET", url, headers=headers)
                print(response.text)



        return HttpResponse("===")

    except Exception as e:
        print(e)

def tests(request):
    return HttpResponse("tests")

def articles(request):
    return HttpResponse("articles")
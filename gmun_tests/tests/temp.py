import requests, random
access_token = "9d26861b7c600e7aa1a8f5f64d9cf167e360d7a3744a188e6c63aff86facfddeb45ac0032f8135fa4b5ec"

text = "wewefw2erfwe"
event_id = "sgrwerw4gr4wrg4"
url = "https://api.vk.com/method/messages.sendMessageEventAnswer?user_id=585675&v=5.120&"+\
      f"access_token={access_token}" \
      "&peer_id=585675&event_data={\"type\": \"show_snackbar\",\"text\": \""+f"{text}"+"\"}" \
      "&event_id=" + f"{event_id}"
response = requests.request("GET", url)
print(response.text.encode('utf8'))
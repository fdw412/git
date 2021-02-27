import os
import json
import requests

from datetime import datetime, timedelta

from gmun_tests.settings import MATTERMOST_URL, MATTERMOST_TEAM, MATTERMOST_TOKEN, ACK_MSG


channel_town_square = 'k4u43q3jrfrh8citcjsnc1ebqw'
channel_alert = 'kcm8c64scb8djp6rd6wfmyspnh'
channel_no_alert = 'fkipqeakxjnm7b9jb1o7p7t4we'
channel_test_fails = 'r1y5g4jnqbrdipiyc4aypg16cc'
channel_test_logs = 'kywpsa13ntnk9qiny957jenz9c'
class Mattermost:

    def __init__(self, token=None):
        self.token = token or MATTERMOST_TOKEN
        self.session = requests.Session()

    def send_message(self, channel_name, message, file_paths=None, token=None):
        team_id = self.get_team_by_name(MATTERMOST_TEAM, token)
        channel_id = self.get_channel_by_name(team_id, channel_name, token)
        post_id = self.create_post(channel_id, message, file_paths, token)
        return post_id

    def create_post(self, channel_id, message, file_paths=None, token=None):
        if not token:
            token = MATTERMOST_TOKEN
        s = requests.Session()
        s.headers.update({"Authorization": f"Bearer {token}"})

        post_data = {
            "channel_id": channel_id,
            "message": message,
        }
        if file_paths and len(file_paths) > 0:
            mattermost_file_ids = []
            for file_path in file_paths:
                if len(mattermost_file_ids) > 4:
                    break
                form_data = {
                    "channel_id": ('', channel_id),
                    "client_ids": ('', "id_for_the_file"),
                    "files": (os.path.basename(file_path), open(file_path, 'rb')),
                }
                r = s.post(MATTERMOST_URL + '/api/v4/files', files=form_data)
                mattermost_file_ids.append(r.json()["file_infos"][0]["id"])

            post_data.update({
                "file_ids": mattermost_file_ids,
            })

        response = s.post(
            MATTERMOST_URL + '/api/v4/posts', data=json.dumps(post_data))
        if response.status_code == 201:
            return json.loads(response.text)['id']
        else:
            return json.loads(response.text)

    def get_posts_from_time(self, channel_id, token=None, from_time=None):
        if not from_time:
            from_time = int((datetime.now() - timedelta(minutes=5)).timestamp())
        url = f'channels/{channel_id}/posts?since={from_time*1000}'
        print(url)
        response = self.get_url_data(url, token)
        return response

    def get_posts_after_post(self, channel_id, post_id, token=None):
        url = f'channels/{channel_id}/posts?after={post_id}'
        response = self.get_url_data(url, token)
        return response

    def get_url_data(self, url, token=None):
        if not token:
            token = MATTERMOST_TOKEN
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        response = requests.get(
            f'{MATTERMOST_URL}/api/v4/{url}',
            headers=headers,
        )
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return response

    def get_teams(self, token=None):
        return self.get_url_data('teams', token)

    def get_team_by_name(self, name, token=None):
        url = f'teams/name/{name}'
        return self.get_url_data(url, token)['id']

    def get_channel_by_name(self, team_id, channel_name, token=None):
        url = f'teams/{team_id}/channels/name/{channel_name}'
        return self.get_url_data(url, token)['id']

    def get_user_info(self, user_id=None, token=None):
        if user_id:
            url = f'users/{user_id}'
        else:
            url = 'users/me'
        return self.get_url_data(url, token)

    def test_ack(self, message):
        ack = False
        if message.find(ACK_MSG) > -1:
            ack = True
        return ack

    def check_message_ack(self, channel_id, checking_post_id):
        posts = self.get_posts_after_post(channel_id, checking_post_id)
        ack = False
        for post in posts['order']:
            post_info = posts['posts'][post]
            user_name = self.get_user_info(post_info['user_id'])['username']
            message = post_info['message']
            if self.test_ack(message) \
                    and post_info['parent_id'] == checking_post_id:
                self.create_post(channel_id, f"Sank you for reply {user_name}")
                ack = True
                break
        return ack

    # def pin_post(self, post_id, token=None):
    #     if not token:
    #         token = MATTERMOST_TOKEN
    #
    #     s.headers.update({"Authorization": f"Bearer {token}"})
    #     response = s.post(MATTERMOST_URL + f'/api/v4/posts/{post_id}/pin')
    #     if response.status_code == 200:
    #         return json.loads(response.text)['status']
    #     else:
    #         return json.loads(response.text)

    def celery_exception_send(self, text):
        # channel_id = 'k4u43q3jrfrh8citcjsnc1ebqw' # town square
        channel_id = 'r1y5g4jnqbrdipiyc4aypg16cc'  # test fails
        Mattermost().create_post(channel_id=channel_id, message=f"celery task exception, {text}")


if __name__ == '__main__':
    # m = Mattermost()
    # channel_id = 'k4u43q3jrfrh8citcjsnc1ebqw' # town square
    # channel_id = 'kcm8c64scb8djp6rd6wfmyspnh' # ms_send_test channel
    # channel_id = 'fkipqeakxjnm7b9jb1o7p7t4we' #test4
    # channel_id = 'r1y5g4jnqbrdipiyc4aypg16cc' # test fails

    # inter_result = {'result': True, 'error': 'эмулиция ошибки', 'screen_paths':
    #     ['D:\\PycharmProjects\\git\\gmun_tests\\settings\\..\\screenshots\\05_12_12_36_01_mcsec_876702.png',
    #      'D:\\PycharmProjects\\git\\gmun_tests\\settings\\..\\screenshots\\05_12_12_36_01_mcsec_876702.png',
    #      'D:\\PycharmProjects\\git\\gmun_tests\\settings\\..\\screenshots\\05_12_12_34_40_mcsec_179029.png',
    #      'D:\\PycharmProjects\\git\\gmun_tests\\settings\\..\\screenshots\\05_12_12_34_40_mcsec_179029.png'],
    #                 'comment': '*gid 164179533, скрипт отправляет сообщение с random id из приложения через рассыльщик '
    #                            'и проверяет его доставку в диалоге, лимит ожидания 300 секунд\n*переход в iframe, попытка 0 ok, '
    #                            'загрузка вкладки создания рассылки ok,  поле выбор темы ok, выбор темы ok, очистка поля сообщения ok, '
    #                            'вставка сообщения в поле ok, отправка рассылки ok, появление отправки в истории ok, проверка доставки ок'}
    # failcount = 3
    # name = 'TestName'
    # channel_id = 'kcm8c64scb8djp6rd6wfmyspnh'
    # message = f"{name} fails {failcount} times\n{inter_result['error']}\n{inter_result['comment']}"
    # # m.create_post(channel_id, message)
    # screen_paths = inter_result['screen_paths']
    # m.create_post(channel_id, message, screen_paths)
    1

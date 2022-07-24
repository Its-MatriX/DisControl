request_bad = [403, 404, 401, 429]


import requests


class Client:


    class Exceptions:
        class FailedToRunClient(Exception):
            pass

        class FailedToSendMessage(Exception):
            pass


    def __init__(self, token, show_logs: bool = True):
        self.token = token
        self.show_logs = show_logs

        Headers = {'Authorization': token}
        test_request = requests.get(
            f'https://discord.com/api/v9/users/@me/library', headers=Headers)

        try:
            error = test_request.json()['message']

            if test_request.status_code in request_bad:
                raise self.Exceptions.FailedToRunClient(
                    f'Failed to run client ({error})')
        except:
            pass


    def send_message(self, channel_id: int, content):

        Json = {'content': content}
        Headers = {'Authorization': self.token}
        Url = f'https://discord.com/api/v9/channels/{channel_id}/messages'

        request = requests.post(Url, json=Json, headers=Headers)

        if self.show_logs:
            if request.status_code in request_bad:
                raise self.Exceptions.FailedToSendMessage(
                    f'Send message error: {request.status_code} - ' +
                    request.json()['message'], request.status_code)
            else:
                print('[i] Send message:', request.status_code)

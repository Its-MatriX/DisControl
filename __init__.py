request_bad = [403, 404, 401, 429]

import requests


class errors:

    class FailedToRunClient(Exception):
        pass

    class FailedToSendMessage(Exception):
        pass

    class FailedToDeleteMessage(Exception):
        pass

    class FailedToEditMessage(Exception):
        pass

    class InvalidStatusIcon(Exception):
        pass

    class FailedToChangeStatusIcon(Exception):
        pass

    class FailedToChangeStatusText(Exception):
        pass


class Status:
    online = 'online'
    idle = 'idle'
    dnd = 'dnd'
    invisible = 'invisible'


class Message:

    def __init__(self, message_id, channel_id, client):
        self.message_id = message_id
        self.channel_id = channel_id
        self.client = client

    def edit(self, new_text):
        Url = f'https://discord.com/api/v9/channels/{self.channel_id}/messages/{self.message_id}'
        Headers = {'Authorization': self.client.token}
        Json = {'content': new_text}

        Request = requests.patch(Url, json=Json, headers=Headers)

        if self.client.show_logs:
            if Request.status_code in request_bad:
                raise errors.FailedToEditMessage(
                    f'Edit message error: {Request.status_code} - ' +
                    Request.json()['message'], Request.status_code)
            else:
                print('[i] Edit message:', Request.status_code)

        return 0

    def delete(self):
        Headers = {'Authorization': self.client.token}
        Url = f'https://discord.com/api/v9/channels/{self.channel_id}/messages/{self.message_id}'
        Request = requests.delete(Url, headers=Headers)

        if self.client.show_logs:
            if Request.status_code in request_bad:
                raise errors.FailedToDeleteMessage(
                    f'Delete message error: {Request.status_code} - ' +
                    Request.json()['message'], Request.status_code)
            else:
                print('[i] Delete message:', Request.status_code)

        return 0


class Client:

    def __init__(self, token, show_logs: bool = True):
        self.token = token
        self.show_logs = show_logs

        Headers = {'Authorization': token}
        TestRequest = requests.get(
            f'https://discord.com/api/v9/users/@me/library', headers=Headers)

        try:
            error = TestRequest.json()['message']

            if TestRequest.status_code in request_bad:
                raise errors.FailedToRunClient(
                    f'Failed to run client ({error})')
        except:
            pass

    def send_message(self, channel_id: int, content):
        Json = {'content': content}
        Headers = {'Authorization': self.token}
        Url = f'https://discord.com/api/v9/channels/{channel_id}/messages'

        Request = requests.post(Url, json=Json, headers=Headers)

        if self.show_logs:
            if Request.status_code in request_bad:
                raise errors.FailedToSendMessage(
                    f'Send message error: {Request.status_code} - ' +
                    Request.json()['message'], Request.status_code)
            else:
                print('[i] Send message:', Request.status_code)

        id = Request.json()['id']

        return Message(id, channel_id, self)

    def set_status_icon(self, status):
        if status not in [
                Status.online, Status.idle, Status.dnd, Status.invisible
        ]:
            raise errors.InvalidStatusIcon('Invalid status icon')

        Url = 'https://discord.com/api/v9/users/@me/settings'
        Headers = {'Authorization': self.token}
        Json = {'status': status}

        Request = requests.patch(Url, headers=Headers, json=Json)

        if self.show_logs:
            if Request.status_code in request_bad:
                raise errors.FailedToChangeStatusIcon(
                    f'Change status icon error: {Request.status_code} - ' +
                    Request.json()['message'], Request.status_code)
            else:
                print('[i] Change status icon:', Request.status_code)

    def set_status_text(self, text):
        Url = 'https://discord.com/api/v9/users/@me/settings'
        Headers = {'Authorization': self.token}
        Json = {'custom_status': {'text': text}}

        Request = requests.patch(Url, headers=Headers, json=Json)

        if self.show_logs:
            if Request.status_code in request_bad:
                raise errors.FailedToChangeStatusText(
                    f'Change status text error: {Request.status_code} - ' +
                    Request.json()['message'], Request.status_code)
            else:
                print('[i] Change status text:', Request.status_code)

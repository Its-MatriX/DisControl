from discontrol.Http import DiscordRequest
# from Channel import Channel
# from threading import Thread


class Guild:

    def __init__(self, guild_id, client):
        self.guild_id = guild_id

        Request = DiscordRequest({}, f'guilds/{guild_id}', client.token)
        Request = Request.get()

        Json = Request.json()
        self.Client = client
        self.id = Json['id']
        self.name = Json['name']
        self.icon = Json['icon']
        self.description = Json['description']
        self.premius_progress_bar_enabled = Json[
            'premium_progress_bar_enabled']
        self.nsfw = Json['nsfw']
        self.nsfw_level = Json['nsfw_level']
        self.mfa_level = Json['mfa_level']
        self.max_members = Json['max_members']
        self.rules_channel_id = Json['rules_channel_id']
        self.locale = Json['preferred_locale']

    def get_guild_users(self):
        body = {

        }

        req = DiscordRequest(body,f'guilds/{self.id}/members',self.Client.token)
        resp = req.post()
        print(resp.json()) 
         # тут !!!!!!!!!!!!!!!!!!! пасс ебари пон а мне что делать дрочить? да пизда пон body-positive ща создам тест пон и еше запусти 
         # у меня расширение не качается

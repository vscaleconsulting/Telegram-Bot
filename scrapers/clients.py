from telethon import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError, PeerFloodError, UserBotError, UserPrivacyRestrictedError, \
    UserNotMutualContactError
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, CreateChannelRequest, \
    InviteToChannelRequest, UpdateUsernameRequest, CheckUsernameRequest, EditPhotoRequest, EditAdminRequest, DeleteMessagesRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest, ExportChatInviteRequest
from time import sleep
from telethon.tl.types import ChannelParticipantsAdmins, ChatAdminRights
from telethon import types
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest


class TGClient:
    """Telethon Client
    """

    def __init__(self, name, api_id, api_hash, bot_token=None):
        """Constructor

        Args:
            name (str): Name
            api_id (int): API ID
            api_hash (str): API Hash
            bot_token (str, optional): bot token. Defaults to None.
        """
        self.name = name
        self.__api_id = api_id
        self.__api_hash = api_hash

        if bot_token is None:
            self.client = TelegramClient(name, api_id, api_hash)
        else:
            self.client = TelegramClient(name, api_id, api_hash).start(bot_token=bot_token)

        self.connect()

    def get_me(self):
        with self.client as client:
            client.loop.run_until_complete(self.__get_me())
        return self.__ret

    def join(self, channel):
        """Joins the Telegram channel

        Args:
            channel (str): channel link
        """
        with self.client as client:
            try:
                client.loop.run_until_complete(self.__join(channel))
            except FloodWaitError as e:
                print('Waiting for {} seconds...'.format(e.seconds))
                sleep(e.seconds)
                self.join(channel)
            except BufferError:
                pass
            except Exception as e:
                print(e)

    def leave(self, channel):
        """Leaves the Telegram channel

        Args:
            channel (str): channel link
        """
        with self.client as client:
            try:
                client.loop.run_until_complete(self.__leave(channel))
            except FloodWaitError as e:
                print('Waiting for {} seconds...'.format(e.seconds))
                sleep(e.seconds)
                self.leave(channel)

    def get_admins(self, group):
        """Gets list of admins of the group

        Args:
            group (str/Channel/Entity): group link, name in member or object

        Returns:
            list<User>: list of objects of class User
        """
        with self.client as client:
            client.loop.run_until_complete(self.__get_users(group, True))
        return self.__ret

    def get_users(self, group):
        """Gets list of users in the group

        Args:
            group (str/Channel/Entity): group link, name in member or object

        Returns:
            list<User>: list of objects of class User
        """
        with self.client as client:
            client.loop.run_until_complete(self.__get_users(group))
        return self.__ret

    def get_entity(self, peer):
        """Gets object for the peer

        Args:
            peer (str/PeerUser/PeerChat/PeerChannel): link or object

        Returns:
            User/Chat/Channel: Entity for the peer passed
        """
        with self.client as client:
            client.loop.run_until_complete(self.__get_entity(peer))
        return self.__ret

    def send_message(self, user, msg):
        """Sends message to user, group or channel

        Args:
            user (str/User/Channel): username or link of the channel, chat
            msg (str): message to be sent

        Returns:
            Status/int: Status if sending message was successful
                        -2 if FloodWaitError exception was raised
                        -1 if any other exception was raised
        """
        with self.client as client:
            client.loop.run_until_complete(self.__send_message(user, msg))
        return self.__ret

    def delete_messages(self, peer, ids):
        with self.client as client:
            client.loop.run_until_complete(self.__delete_messages(peer, ids))

    def forward_messages(self, user, msg):
        """Forwards message to the user

        Args:
            user (str/Entity): peer link or object
            msg (Message): message to be forwarded

        Returns:
            Status/int: Status if sending message was successful
                        -2 if FloodWaitError exception was raised
                        -1 if any other exception was raised
        """
        with self.client as client:
            client.loop.run_until_complete(self.__forward_messages(user, msg))
        return self.__ret

    def pin_message(self, peer, id):
        """Pins the message in Group or Channel

        Args:
            peer (str/Entity): group/channel link or object
            id (int): id of the message to be pinned
        """
        with self.client as client:
            client.loop.run_until_complete(self.__pin_message(peer, id))

    def update_profile(self, first_name=None, last_name=None, about=None):
        """Updates the First name, Last name and About section of the session user

        Args:
            first_name (str, optional): first name. Defaults to None.
            last_name (str, optional): last name. Defaults to None.
            about (str, optional): about. Defaults to None.

        Raises:
            Exception: when all the values passed are None
        """
        d = dict()
        if first_name is not None:
            d['first_name'] = first_name
        if last_name is not None:
            d['last_name'] = last_name
        if about is not None:
            d['about'] = about
        if len(d) == 0:
            raise Exception
        with self.client as client:
            client.loop.run_until_complete(self.__update_profile(**d))

    def update_picture(self, file_path):
        """Updates the profile picture of the session user

        Args:
            file_path (str): path to the image file
        """
        with self.client as client:
            client.loop.run_until_complete(self.__update_picture(file_path))

    def get_chat_messages(self, chat, limit=1):
        """Gets the latest messages in the chat/channel

        Args:
            chat (link/Entity): link or Entity of the chat/channel
            limit (int, optional): number of messsages to get. Gets all if set to None. Defaults to 1.

        Returns:
            list<Message>: list of messages
        """
        with self.client as client:
            client.loop.run_until_complete(self.__get_chat_messages(chat, limit))
        return self.__ret

    def create_channel(self, title, about, username=None, photo=None):
        """Creates channel with the given title, about section and photo. The channel is private by default and is set to public if username is not None

        Args:
            title (str): name of the channel
            about (str): about
            username (str, optional): username of the channel. Defaults to None.
            photo (str, optional): path to the image file. Defaults to None.

        Returns:
            bool: True if channel was created successfully else False (if username is not available)
        """
        with self.client as client:
            client.loop.run_until_complete(self.__create_channel(title, about, username, photo))
        return self.__ret

    def invite_to_channel(self, channel_name, users):
        """Adds user to channel/group

        Args:
            channel_name (str/Entity): link or Entity of the group/channel
            users (list<str/User/PeerUser>): list of users

        Returns:
            Status/int: Status object if no exception is raised
                        -3 if PeerFloodError occurs
                        -4 if UserbotError occurs
                        -5 if UserPrivacyRestrictedError occurs
                        -6 if UserNotMutualContactError occurs
        """
        with self.client as client:
            client.loop.run_until_complete(self.__invite_to_channel(channel_name, users))
        return self.__ret

    def update_channel_username(self, channel, username):
        """Updates channel username and sets the channel/group to public if private

        Args:
            channel (str/Entity): name/link/Entity of the channel
            username (str): username

        Returns:
            bool: True if successful else False (if username is not available)
        """
        with self.client as client:
            client.loop.run_until_complete(self.__update_channel_username(channel, username))
        return self.__ret

    def update_channel_photo(self, channel, file_path):
        """Update picture of the channel/group

        Args:
            channel (str/Entity): name, link or Entity of group/channel
            file_path (str): path to the image file
        """
        with self.client as client:
            client.loop.run_until_complete(self.__update_channel_photo(channel, file_path))

    def get_link(self, peer):
        """Gets link of the User/Channel/Chat

        Args:
            peer (str/Entity): username or Entity

        Returns:
            str: link to the peer
        """
        with self.client as client:
            client.loop.run_until_complete(self.__get_link(peer))
        return self.__ret

    def update_admin_rights(self, channel, user, **kwargs):
        """Updates the rights of the admin in a group/channel. Can be used to add new users or bots as admins

        Args:
            channel (str/Entity): link or Entity of the channel/group
            user (str/User/PeerUser): user/bot
        """
        rights = ChatAdminRights(**kwargs)
        with self.client as client:
            client.loop.run_until_complete(self.__update_admin_rights(channel, user, rights))

    def connect(self):
        """Connects and diconnects the client
        """
        with self.client as client:
            pass

    def get_session_str(self,get_str=False):
        if(get_str):
            return self.client.session
        return StringSession.save(self.client.session)

    def is_restricted(self):
        self.send_message('@SpamBot', '/start')
        sleep(1)
        message = self.get_chat_messages('@SpamBot')[0].message
        return not message.startswith('Good news')

    async def __get_me(self):
        self.__ret = await self.client.get_me()

    async def __join(self, channel):
        await self.client(JoinChannelRequest(channel))

    async def __leave(self, channel):
        await self.client(LeaveChannelRequest(channel))

    async def __get_users(self, channel, admins_only=False):
        try:
            if admins_only:
                self.__ret = await self.client.get_participants(channel, filter=ChannelParticipantsAdmins)
            else:
                self.__ret = await self.client.get_participants(channel)
        except FloodWaitError as e:
            print(e)
            self.__ret = -2
        except Exception as e:
            print(e)
            self.__ret = -1

    async def __get_entity(self, channel):
        try:
            self.__ret = await self.client.get_entity(channel)
        except FloodWaitError as e:
            print(e)
            self.__ret = -2
        except Exception as e:
            print(e)
            self.__ret = -1

    async def __send_message(self, user, msg):
        try:
            self.__ret = await self.client.send_message(user, msg)
        except FloodWaitError as e:
            print(e)
            self.__ret = -2
        except Exception as e:
            print(e)
            self.__ret = -1

    async def __delete_messages(self, peer, ids):
        await self.client.delete_messages(peer, ids)

    async def __forward_messages(self, user, msg):
        try:
            await self.client.forward_messages(user, msg)
            self.__ret = 0
        except FloodWaitError as e:
            print(e)
            self.__ret = -2
        except Exception as e:
            print(e)
            self.__ret = -1

    async def __pin_message(self, peer, id):
        await self.client(UpdatePinnedMessageRequest(peer, id))

    async def __update_profile(self, **kwargs):
        await self.client(UpdateProfileRequest(**kwargs))

    async def __update_picture(self, file_path):
        await self.client(UploadProfilePhotoRequest(await self.client.upload_file(file_path)))

    async def __get_chat_messages(self, chat, limit):
        self.__ret = await self.client.get_messages(chat, limit)

    async def __create_channel(self, title, about, username, photo):
        await self.client(CreateChannelRequest(title=title, about=about, broadcast=True, for_import=True))

        if photo is not None:
            await self.client(EditPhotoRequest(channel=title, photo=await self.client.upload_file(photo)))

        if username is not None:
            self.__ret = await self.client(CheckUsernameRequest(title, username))
            if self.__ret:
                await self.__update_channel_username(title, username)
        else:
            self.__ret = True

    async def __invite_to_channel(self, channel_name, users):
        try:
            t = await self.client(InviteToChannelRequest(channel=channel_name, users=users))
            self.__ret = t
        except PeerFloodError:
            self.__ret = -3
        except UserBotError:
            self.__ret = -4
        except UserPrivacyRestrictedError:
            self.__ret = -5
        except UserNotMutualContactError:
            self.__ret = -6
        except Exception as e:
            print(e)
            print(users)
            self.__ret = -1

    async def __update_channel_username(self, channel_name, username):
        self.__ret = await self.client(CheckUsernameRequest(channel_name, username))
        if self.__ret:
            await self.__update_channel_username(channel_name, username)

    async def __update_channel_photo(self, channel_name, file_path):
        await self.client(EditPhotoRequest(channel=channel_name, photo=await self.client.upload_file(file_path)))

    async def __get_link(self, peer):
        self.__ret = await self.client(ExportChatInviteRequest(peer))

    async def __update_admin_rights(self, channel, user, rights):
        await self.client(EditAdminRequest(channel, user, rights, rank='qweret'))

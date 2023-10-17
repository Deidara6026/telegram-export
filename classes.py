from telethon.sync import TelegramClient  # Importing the TelegramClient from telethon.sync
import json  # Importing the json module
import config  # Importing the config module
import logging  # Importing the logging module
from telethon import errors
import asyncio


logging.basicConfig(filename="export.log",  # Setting up the basic configuration for logging
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.WARNING)


class Spyder():
    crawl_list = []

    def __init__(self, name, api_key, api_hash):
        self.api_key = api_key
        self.api_hash = api_hash
        self.name = name
        self.client = None
    
    async def initialize(self) -> TelegramClient:
        """
        Start the client and assign it to the class instance
        """
        client = TelegramClient(self.name, api_id=self.api_key, api_hash=self.api_hash, proxy=config.proxy, flood_sleep_threshold=1000)
        print("Beginning log in sequence for ", self.name)
        await client.start(phone=self.name)
        print("\n")
        await asyncio.sleep(1)
        self.client = client
        return client

    async def _dump_all_messages(self, chat_name):  # Defining an asynchronous function to dump all messages from the specified chats
        try:
            all_messages = []
            async for message in self.client.iter_messages(chat_name):  # Asynchronously iterating over each message in the chat
                data = message.to_dict()  # Converting the message to a dictionary
                try:
                    _message = {"text":data["message"], "timestamp":data["date"].strftime("%m/%d/%Y, %H:%M:%S"), "message_id":data["id"]}  # Creating a dictionary to store the message text, timestamp, and id
                except Exception as e:  # Handling any exceptions that may occur
                    continue  # Continuing to the next iteration if an exception occurs
                
                try:
                    _message.update({"author_id":data["from_id"]["user_id"]})  # Updating the message dictionary with the author's id
                except KeyError:  # Handling a KeyError exception
                    _message.update({"author_id":data["from_id"]["channel_id"]})  # Updating the message dictionary with the channel id if a KeyError occurs
                
                try:
                    _message.update({"reply_to_message":data.get("reply_to").get("reply_to_msg_id")})  # Updating the message dictionary with the id of the message it is replying to
                except AttributeError:  # Handling an AttributeError exception
                    _message.update({"reply_to_message":"None"})  # Updating the message dictionary with 'None' if an AttributeError occurs
                    pass

                print(f"{self.name} - {chat_name} - {len(all_messages)}")  # Printing the number of messages
                all_messages.append(_message)  # Appending the message dictionary to the list of all messages


            with open(chat_name.replace("https://t.me/", "").strip("+")+'-messages.json', 'w') as f:  # Opening a file to write the messages to
                json.dump(all_messages, f)  # Dumping the list of all messages to the file
        except Exception as e:  # Handling any exceptions that may occur
            logging.error(e.__repr__())  # Logging the exception
    
    # async def crawl(self):
    #     x = []
    #     try:
    #         for i in range(config.spiders_per_phone):
    #             chat = self.crawl_list.pop()
    #             x.append(self._dump_all_messages(chat))
    #         await asyncio.gather(*x)
    #     except IndexError as e:
    #         if len(x) == 0:
    #             print("Operation complete")
    #         else:
    #             await asyncio.gather(*x)
                




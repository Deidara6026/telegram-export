from classes import Spyder
import config
import asyncio

async def main():
    with open("links.txt", "r") as f:
        links = f.readlines()
        Spyder.crawl_list = links
        web = []
        for i in config.phone_list:
            c = Spyder(i, config.api_id, config.api_hash)
            await c.initialize()

            web.append(c)
        x = []
        while Spyder.crawl_list:
            for i in range(config.spiders_per_phone):
                for spyder in web:
                    if Spyder.crawl_list:  # Check if the list is not empty
                        chat = Spyder.crawl_list.pop()
                        x.append(spyder._dump_all_messages(chat))
            if x:  # If there are tasks to gather
                await asyncio.gather(*x)
            else:
                print("Operation complete")

        

if __name__=="__main__":
    asyncio.run(main())

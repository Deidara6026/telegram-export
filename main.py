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
        await asyncio.gather(*[spyder._dump_all_messages(spyder.crawl_list.pop()) for spyder in web for i in range(config.spiders_per_phone)])

if __name__=="__main__":
    asyncio.run(main())

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
        await asyncio.gather(*[spyder.crawl() for spyder in web])

if __name__=="__main__":
    asyncio.run(main())

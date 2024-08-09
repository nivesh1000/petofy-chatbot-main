from webscrape import WebScrape
import os
from chroma import Chromaappender
from response import Response
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"



db_name = "petofy_cdb"
dbloc = "staticdata"
scrapedataloc="staticdata/crawled_data.txt"
sitemap_url="https://www.petofy.com/sitemap.xml"

if os.path.getsize(scrapedataloc) == 0:
    WebScrape(sitemap_url,scrapedataloc)

robj=Response()


cobj=Chromaappender(db_name,dbloc,scrapedataloc)
while True:
    query=input("Query>> ")
    if(query.strip()=='exit'):
        break
    similar_results=cobj.similarity_search(query)
    response=robj.chat_completion(query,similar_results)
    print(f"Response>> {response}")




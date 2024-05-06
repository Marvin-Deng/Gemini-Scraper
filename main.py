from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from crawler.crawler import Crawler

app = FastAPI()


class CrawlRequest(BaseModel):
    url: str
    topics: list
    max_depth: int


@app.post("/crawl/")
async def crawl(request: CrawlRequest):
    try:
        crawler = Crawler(request.url, request.topics, request.max_depth)
        result = crawler.bfs_crawl()
        print(result)
        return JSONResponse(
            status_code=200, content={"data": result}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": f"An error occurred: {str(e)}"}
        )

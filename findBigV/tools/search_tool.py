from langchain.utilities import SerpAPIWrapper
import os


def get_UID(flower: str):
    search = SerpAPIWrapper(serpapi_api_key=os.environ.get("SERPAPI_API_KEY"))
    res = search.run(f"{flower}")
    return res
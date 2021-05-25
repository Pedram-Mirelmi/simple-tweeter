from typing import Union

from .ClientKeywords import *
from .RH_client import RequestHandler


class BaseBackendApp:
    def __init__(self, port: int = 9990, max_req_len: int = 4):
        self.user_info = {USERNAME: str(),
                          PASSWORD: str()}
        self.req_handler = RequestHandler(self.user_info, port, max_req_len)
        self._max_req_len = max_req_len

    def _getAllTweet(self) -> list[dict[str, Union[str, int]]]:
        response = self.req_handler.allTweets()
        print(response)
        return response

    def _likeTweet(self, tweet_id: int) -> dict[str]:
        response = self.req_handler.likeTweet(tweet_id)
        print(response)
        return response

    def _writeNewTweet(self, tweet_text: str) -> dict[str]:
        response = self.req_handler.newTweet(tweet_text)
        return response

    def _register(self, username: str, name: str, password: str) -> dict[str]:
        return self.req_handler.register({REQUEST_TYPE: LOGIN,
                                          USERNAME: username,
                                          NAME: name,
                                          PASSWORD: password})

    def _login(self, username: str, password: str) -> dict[str]:
        return self.req_handler.login({REQUEST_TYPE: LOGIN,
                                       USERNAME: username,
                                       PASSWORD: password})

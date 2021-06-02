import socket
from .ClientKeywords import *
from typing import Union
import json


class RequestHandler:
    def __init__(self, user_info: dict[str, str], port: int = 9999, max_req_len: int = 5):
        self.user_info = user_info
        self._max_req_len = max_req_len
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect(("localhost", port))

    def getTweetInfo(self, tweet_id: int):
        return self._send({
            REQUEST_TYPE: TWEET_INFO,
            TWEET_ID: tweet_id
        })

    def updateProfile(self, profile_info):
        return self._send({
            REQUEST_TYPE: UPDATE_PROFILE,
            USER_ID: self.user_info[USER_ID],
            PROFILE_INTO: profile_info
        })

    def getComments(self, tweet_id) -> list[dict[str, str]]:
        return self._send({
            REQUEST_TYPE: GET_COMMENTS,
            TWEET_ID: tweet_id
        })

    def likeTweet(self, tweet_id: int) -> dict[str, str]:
        return self._send({
            REQUEST_TYPE: LIKE_TWEET,
            TWEET_ID: tweet_id,
            USER_ID: self.user_info[USER_ID]
        })

    def likeComment(self, comment_id: int) -> dict[str, str]:
        return self._send({
            REQUEST_TYPE: LIKE_COMMENT,
            COMMENT_ID: comment_id,
            USER_ID: self.user_info[USER_ID]
        })

    def addComment(self, comment_text: str, tweet_id: int) -> dict[str, str]:
        return self._send({
            REQUEST_TYPE: NEW_COMMENT,
            USER_ID: self.user_info[USER_ID],
            TWEET_ID: tweet_id,
            COMMENT_TEXT: comment_text
        })

    def newTweet(self, tweet_text: str) -> dict[str, str]:
        return self._send({
            USER_ID: self.user_info[USER_ID],
            REQUEST_TYPE: NEW_TWEET,
            TWEET_TEXT: tweet_text
        })

    def newComment(self, comment_text: str, tweet_id: int) -> dict[str, str]:
        return self._send({
            REQUEST_TYPE: NEW_COMMENT,
            TWEET_ID: tweet_id,
            COMMENT_TEXT: comment_text,
            USER_ID: self.user_info[USER_ID]
        })

    def userTweets(self, user_id: int) -> list[dict[str, str]]:
        return self._send({
            REQUEST_TYPE: USER_TWEETS,
            USER_ID: user_id
        })

    def getAllTweets(self) -> list[dict[str, str]]:
        return self._send({REQUEST_TYPE: ALL_TWEETS})

    def login(self, user_info: dict) -> dict[str, str]:
        user_info[REQUEST_TYPE] = LOGIN
        return self._send(user_info)

    def register(self, user_info) -> dict[str, str]:
        user_info[REQUEST_TYPE] = REGISTER
        return self._send(user_info)

    def __getRes(self) -> Union[list, dict]:
        req_len = int(self._sock.recv(self._max_req_len).decode('utf-8'))
        return json.loads(self._sock.recv(req_len).decode('utf-8'))

    def _send(self, req_dic: dict) -> Union[list, dict]:
        self.__sendReq(req_dic)
        return self.__getRes()

    def __sendReq(self, res_dic: dict) -> None:
        res_str = json.dumps(res_dic)
        res_str = f"{len(res_str):<{self._max_req_len}}" + res_str
        print(f'sending: {res_str}')
        self._sock.send(bytes(res_str, encoding='utf-8'))

    def setUserInfo(self, user_info: dict) -> None:
        self.user_info = user_info

    def terminate(self) -> None:
        print('terminating...')
        self.__sendReq({})
        self._sock.close()

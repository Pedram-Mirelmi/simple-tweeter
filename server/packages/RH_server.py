import json

from client.BackendPackages.ClientKeywords import *
from mysql.connector import Error as DBError, connect
from typing import Union, Any


class RequestHandler:
    def __init__(self):
        self.connection = connect(host='localhost',
                                  user='root',
                                  password='parotholandi',
                                  database='tweeter')
        self.cursor = self.connection.cursor(dictionary=True)

    def handle(self, request: dict) -> Union[dict, list]:
        self.cursor.reset(True)
        if request[REQUEST_TYPE] == REGISTER:
            return self._register(request)
        if request[REQUEST_TYPE] == LOGIN:
            return self._login(request)
        if request[REQUEST_TYPE] == NEW_TWEET:
            return self._new_tweet(request)
        if request[REQUEST_TYPE] == ALL_TWEETS:
            return self._allTweets()
        if request[REQUEST_TYPE] == LIKE_TWEET:
            return self._likeTweet(request)
        if request[REQUEST_TYPE] == NEW_COMMENT:
            return self._newComment(request)
        if request[REQUEST_TYPE] == GET_COMMENTS:
            return self._getComments(request)
        if request[REQUEST_TYPE] == USER_TWEETS:
            return self._userTweets(request)
        if request[REQUEST_TYPE] == LIKE_COMMENT:
            return self._likeComment(request)
        if request[REQUEST_TYPE] == UPDATE_PROFILE:
            return self._updateProfile(request)
        if request[REQUEST_TYPE] == TWEET_INFO:
            return self._getTweetInfo(request)
        print(request)
        raise Exception(f'Invalid request: {request}')

    def _getTweetInfo(self, request: dict[str, int]):
        self.cursor.execute(f"{SELECT} * {FROM} tweets_show "
                            f"{WHERE} {TWEET_ID} = {request[TWEET_ID]}")
        response = self.cursor.fetchall()[0]
        response[OUTCOME] = True

        return response

    def _updateProfile(self, request: dict[str, Union[str, dict[str, str]]]) -> dict[str, str]:
        try:
            self.__UPDATE(USERS, request[PROFILE_INTO].items(), USER_ID, request[USER_ID])
            return {OUTCOME: True}
        except DBError as e:
            return {OUTCOME: False, MESSAGE: str(e), ERROR_NO: e.errno}
        except Exception as e:
            return {OUTCOME: False, MESSAGE: f"something went wrong: {e}"}

    def _newComment(self, request: dict) -> dict:
        try:
            self.__INSERT(COMMENTS, (TWEET_ID, USER_ID, COMMENT_TEXT),
                          (request[TWEET_ID], request[USER_ID], request[COMMENT_TEXT]))
            return {OUTCOME: True}
        except DBError as e:
            return {OUTCOME: False, MESSAGE: str(e)}
        except Exception as e:
            return {OUTCOME: False, MESSAGE: f"something went wrong: {e}"}

    def _getComments(self, request: dict) -> list:
        self.cursor.execute(f"{SELECT} * "
                            f"{FROM} comments_show "
                            f"{WHERE} tweet_id = {request[TWEET_ID]};")
        return self.cursor.fetchall()

    def _likeComment(self, request: dict) -> dict[str, str]:
        try:
            self.__INSERT(COMMENTS_LIKES, (USER_ID, COMMENT_ID),
                          (request[USER_ID], request[COMMENT_ID]))
            return {OUTCOME: True}
        except DBError as e:
            return {OUTCOME: False, MESSAGE: str(e)}
        except Exception as e:
            return {OUTCOME: False, MESSAGE: f'Something went wrong: {e}'}

    def _likeTweet(self, request: dict) -> dict:
        try:
            self.__INSERT(TWEETS_LIKES, (USER_ID, TWEET_ID),
                          (request[USER_ID], request[TWEET_ID]))
            return {OUTCOME: True}
        except DBError as e:
            return {OUTCOME: False, MESSAGE: str(e)}
        except Exception as e:
            return {OUTCOME: False, MESSAGE: f'Something went wrong: {e}'}

    def _new_tweet(self, request: dict) -> dict:
        try:
            self.__INSERT('tweets',
                          ('tweet_text', 'user_id'),
                          (request[TWEET_TEXT], request[USER_ID]))
            return {OUTCOME: True}
        except DBError as e:
            return {OUTCOME: False, MESSAGE: str(e)}

    def _allTweets(self) -> list:
        self.cursor.execute(f"{SELECT} * {FROM} tweets_show;")
        return self.cursor.fetchall()

    def _userTweets(self, request: dict[str, str]):
        self.cursor.execute(f"{SELECT} * {FROM} tweets_show "
                            f"{WHERE} user_id = {request[USER_ID]} ")
        return self.cursor.fetchall()

    def _register(self, request: dict) -> dict:
        try:
            self.__INSERT(USERS, ('username', 'password', 'name'),
                          (request[USERNAME], request[PASSWORD], request[NAME]))
            self.cursor.execute(f"{SELECT} * {FROM} users {WHERE} "
                                f"username='{request[USERNAME]}';")
            response = self.cursor.fetchall()[0]
            response[OUTCOME] = True
            response.update(self._getUserInfo(response[USER_ID]))
            return response
        except DBError as e:
            return {OUTCOME: False, MESSAGE: str(e)}

    def _login(self, request: dict) -> dict:
        try:
            self.cursor.execute(f"{SELECT} * {FROM} users {WHERE} "
                                f"username='{request[USERNAME]}'")
            response = self.cursor.fetchall()[0]
            if response[PASSWORD] != request[PASSWORD]:
                return {OUTCOME: False, MESSAGE: E1}
            response[OUTCOME] = True
            response.update(self._getUserInfo(response[USER_ID]))
            return response
        except DBError as db_error:
            return {OUTCOME: False, MESSAGE: str(db_error)}
        except IndexError:
            return {OUTCOME: False, MESSAGE: E2}

    def _getUserInfo(self, user_id: int):
        self.cursor.execute(f"{SELECT} * {FROM} users_show "
                            f"{WHERE} user_id = {user_id} ")
        return self.cursor.fetchall()[0]

    def __INSERT(self, tablename: str, columns: tuple, values: tuple):

        self.cursor.execute(f"{INSERT} {INTO} {tablename} ({', '.join(map(str, columns))}) "
                            f"{VALUES} {values};")
        self.connection.commit()

    def __UPDATE(self, table: str, column_value_pair_list, id_field: str, id_value: Any) -> None:
        self.cursor.execute(f"{UPDATE} {table} {SET} \n     "
                            + ', '.join(
                            [f'{column} = {json.dumps(value)}' for column, value in column_value_pair_list]) +
                            f" {WHERE} {id_field} = {id_value};")
        self.connection.commit()

    def __del__(self):
        self.connection.commit()

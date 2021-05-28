from client.BackendPackages.ClientKeywords import *
from mysql.connector import Error, connect
from typing import Union


class RequestHandler:
    def __init__(self):
        self.connection = connect(host='localhost',
                                  user='root',
                                  password='parotholandi',
                                  database='tweeter')
        self.cursor = self.connection.cursor(dictionary=True)

    def handle(self, request: dict) -> Union[dict, list]:
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
        if request[REQUEST_TYPE] == ADD_COMMENT:
            return self._addComment(request)
        if request[REQUEST_TYPE] == GET_COMMENTS:
            return self._getComments(request)
        if request[REQUEST_TYPE] == USER_TWEETS:
            return self._userTweets(request)
        else:
            print(request)
            raise Exception(f'Invalid request: {request}')

    def _addComment(self, request: dict) -> dict:
        try:
            self.__INSERT(COMMENTS, (TWEET_ID, USER_ID, COMMENT_TEXT),
                          (request[TWEET_ID], request[USER_ID], request[COMMENT_TEXT]))
            return {OUTCOME: True}
        except Error as e:
            return {OUTCOME: False, STATUS: str(e)}
        except Exception as e:
            return {OUTCOME: False, STATUS: f"something went wrong: {e}"}

    def _getComments(self, request: dict) -> list:
        self.cursor.execute(f"{SELECT} "
                            f"      u.{USERNAME}, "
                            f"      c.{COMMENT_TEXT}, "
                            f"      c.{CREATED_AT} "
                            f"{FROM} {COMMENTS} c "
                            f"   {JOIN} {USERS} u "
                            f"      {USING} ({USER_ID}) "
                            f"{WHERE} c.{TWEET_ID} = {request[TWEET_ID]}; ")
        return self.cursor.fetchall()

    def _likeTweet(self, request: dict) -> dict:
        try:
            self.__INSERT(LIKES, (USER_ID, TWEET_ID),
                          (request[USER_ID], request[TWEET_ID]))
            return {OUTCOME: True}
        except Error as e:
            return {OUTCOME: False, STATUS: str(e)}
        except Exception as e:
            return {OUTCOME: False, STATUS: f'Something went wrong: {e}'}

    def _new_tweet(self, request: dict) -> dict:
        try:
            self.__INSERT('tweets',
                          ('tweet_text', 'user_id'),
                          (request[TWEET_TEXT], request[USER_ID]))
            return {OUTCOME: True}
        except Error as e:
            return {OUTCOME: False, STATUS: str(e)}

    def _allTweets(self) -> list:
        self.cursor.execute(f"{SELECT} * {FROM} tweets_show;")
        return self.cursor.fetchall()

    def _userTweets(self, request: dict[str, str]):
        self.cursor.execute(f"{SELECT} * {FROM} tweets_show "
                            f"{WHERE} user_id = {request[USER_ID]}")
        return self.cursor.fetchall()

    def _register(self, request: dict) -> dict:
        try:
            self.__INSERT(USERS, ('username', 'password', 'name'),
                          (request[USERNAME], request[PASSWORD], request[NAME]))
            self.cursor.execute(f"{SELECT} * {FROM} users {WHERE} "
                                f"username='{request[USERNAME]}';")
            response = self.cursor.fetchall()[0]
            response[OUTCOME] = True
            return response
        except Error as e:
            return {OUTCOME: False, STATUS: str(e)}

    def _login(self, request: dict) -> dict:
        try:
            self.cursor.execute(f"{SELECT} * {FROM} users {WHERE} "
                                f"username='{request[USERNAME]}'")
            res_dict = self.cursor.fetchall()[0]
            if res_dict[PASSWORD] != request[PASSWORD]:
                return {OUTCOME: False, STATUS: E1}
            res_dict[OUTCOME] = True
            return res_dict
        except Error as db_error:
            return {OUTCOME: False, STATUS: str(db_error)}
        except IndexError:
            return {OUTCOME: False, STATUS: E2}

    def __INSERT(self, tablename: str, columns: tuple, values: tuple):
        self.cursor.execute(f"{INSERT} {INTO} {tablename} ({', '.join(map(str, columns))}) "
                            f"{VALUES} {values};")
        self.connection.commit()

    def __UPDATEAddOne(self, table: str, column: str, id_field: str, id_value: int) -> dict:
        self.cursor.execute(f'{UPDATE} {table} {SET} {column} = {column} + 1 '
                            f'{WHERE} {id_field} = {id_value};')
        self.connection.commit()
        return {OUTCOME: True}

    def __UPDATESubOne(self, table: str, column: str, id_field: str, id_value: int) -> dict:
        try:
            self.cursor.execute(f'{UPDATE} {table} {SET} {column} = {column} - 1 '
                                f'{WHERE} {id_field} = {id_value};')
            self.connection.commit()
            return {OUTCOME: True}
        except Error as e:
            return {OUTCOME: False, STATUS: str(e)}

    def __del__(self):
        self.connection.commit()

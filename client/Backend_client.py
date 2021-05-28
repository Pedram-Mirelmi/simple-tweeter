from packages.RH_client import RequestHandler
from keywords import *


def getValidIndex(maximum: int, message: str):
    while True:
        index = input(message)
        if index.strip() == '-1':
            return -1
        try:
            integer = int(index)
            if 0 < integer <= maximum:
                return integer
            else:
                print('Not in range!')
        except ValueError:
            print('Enter number, not character')


class App:
    def __init__(self, port: int = 9999, max_req_len: int = 4):
        self._user_info = {USERNAME: str(),
                           PASSWORD: str()}
        self.req_handler = RequestHandler(port, max_req_len)
        self._max_req_len = max_req_len

    def run(self):
        try:
            while USER_ID not in self._user_info:
                self.enterApp()
            self._home()
            self._exitApp()
        except Exception as e:
            print(f'got an error: {e}')
            self._exitApp()

    def _home(self):
        """main environment"""
        while True:
            all_tweets = self.req_handler.getAllTweets()
            App.showTweetsList(all_tweets=all_tweets)
            choice = input('1) to write a new tweet\n'
                           '2) like a tweet\n'
                           '3) select a tweet\n'
                           '4) search for people\n')  # TODO
            while True:
                if choice == '1':
                    self._writeNewTweet()
                    break
                if choice == '2':
                    self._likeTweet(all_tweets)
                    break
                if choice == '3':
                    self._singleTweetEnv(all_tweets)
                    break
                if choice == '4':
                    self._searchMenu()
                    break
                choice = input('wrong choice! try again:')

    def _singleTweetEnv(self, all_tweets: list[dict]):
        tweet_index = getValidIndex(len(all_tweets), 'enter tweet number or -1 to back')
        if tweet_index == -1:
            return
        while True:
            App.showTweetsList([all_tweets[tweet_index - 1]])  # print tweet at top
            all_comments = self.req_handler.getComments(all_tweets[tweet_index - 1][TWEET_ID])
            App.showAllComments(all_comments)  # print comments below the tweet
            choice = getValidIndex(1, 'enter 1 to add comment, -1 to back')
            if choice == -1:
                return
            self._addComment(all_tweets[tweet_index - 1][TWEET_ID])

    @staticmethod
    def showAllComments(all_comments: list):
        for index, comment in enumerate(all_comments):
            print(f'{index + 1}) {comment[USERNAME]} on '
                  f'{comment[CREATED_AT]} commented:\n'
                  f'{comment[COMMENT_TEXT]}\n')

    def _addComment(self, tweet_id: int):
        comment_text = input('write your comment or # to back: ')
        if comment_text.strip() == '#':
            return
        response = self.req_handler.addComment(comment_text, tweet_id)
        print(response)

    def _searchMenu(self):  # TODO complete this function
        pass

    def _likeTweet(self, all_tweets: list[dict]) -> None:
        tweet_index = getValidIndex(len(all_tweets), 'enter the tweet number or -1 to back: ')
        if tweet_index == -1:
            return
        response = self.req_handler.likeTweet(all_tweets[tweet_index - 1][TWEET_ID])
        print(response)

    def _writeNewTweet(self) -> None:
        choice = input('0 to write a tweet, Anything else to back: ')
        if choice != '0':
            return
        tweet_text = input('write your tweet: ')
        response = self.req_handler.newTweet(tweet_text)
        print(response)

    @staticmethod
    def showTweetsList(all_tweets: list) -> None:
        for index, tweet in enumerate(all_tweets):
            print(f'{index + 1}) {tweet[USERNAME]} on '
                  f'"{tweet[CREATED_AT]}" wrote:\n'
                  f'{tweet[TWEET_TEXT]}\n'
                  f'liked by {tweet[LIKES]} people\n')

    def enterApp(self) -> None:
        choice = input('0 to login, 1 to register, 2 to exit: ')
        while True:
            if choice == '0':
                self.login()
                break
            elif choice == '1':
                self.register()
                break
            elif choice == '2':
                self._exitApp()
            else:
                choice = input('wrong choice! try again: ')
        self.req_handler.setUserInfo(self._user_info)

    def register(self) -> None:
        self.getUserPass()
        self._user_info[NAME] = input("name: ")
        response = self.req_handler.register(self._user_info)
        if not response[OUTCOME]:
            print("couldn't register!", response[STATUS])
        else:
            self._user_info = response
            print(f"Successfully registered and logged in{MARK_SIGN}", self._user_info)

    def login(self) -> None:
        self.getUserPass()
        response = self.req_handler.login(self._user_info)
        if not response[OUTCOME]:
            print(f"couldn't login: {response[E_CODE]}")
        else:
            self._user_info = response
            print(f"Successfully logged in{MARK_SIGN}")

    def _exitApp(self) -> None:
        self.req_handler.terminate()
        print('Good bye!')
        exit(0)

    def getUserPass(self) -> None:
        self._user_info[USERNAME] = input('username:')
        self._user_info[PASSWORD] = input('password:')


if __name__ == '__main__':
    app = App()
    app.run()


import tweepy
from com_goldenthinker_trade_datasource.OnDemandDataSource import OnDemandDataSource


class TwitterOnDemandDataSource(OnDemandDataSource):
    
    _instance = None
   
    @classmethod
    def get_instance(cls,profiles=[]):
        if cls._instance is None:
            cls._instance = TwitterOnDemandDataSource(profiles=profiles)
        return cls._instance
        
    
    def __init__(self,profiles=[]):
        super().__init__(name='twitter_elon_musk')
        self.profiles = profiles
        self.api_key = 'v4FSSvLLdovC4TQ9aVt4MrjoV'
        self.api_key_secret = 'yUiLH4Ltzv3LnlBqEfNLAyC3l4AnjDYOjQLdC4OLBuemNNUesa'
        self.bearer_token = 'AAAAAAAAAAAAAAAAAAAAAA99WwEAAAAAuhk7nE7vh1tlyfgO09mXZn2RnHg%3DD87T2L52GYjQfDBKbSReDegMIv43jAnnZwJY6d6D21pg4NzdQU'
        self.access_token_key = '1358222370-jrs4cZhu6g3nOBmZbA8aNy9ZQhVlpDfVd3dD54u'
        self.access_token_key_secret = 'q9mGx5jayK9zbofqKEJQNPX71Wu4QEJX7utBRuBbG93EP'
        self.auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        self.auth.set_access_token(self.access_token_key, self.access_token_key_secret)
        self.api = tweepy.API(self.auth)

    
    
    def update(self,query='elonmusk'):
        tweets = tweepy.Cursor(self.api.user_timeline,id=query).items()
        return tweets
        
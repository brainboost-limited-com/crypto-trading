from com_goldenthinker_trade_datasource.DataSourceManager import DataSourceManager


twitter_ds = DataSourceManager.get_data_source('twitter')

elon_twits = twitter_ds.update()
print(elon_twits)
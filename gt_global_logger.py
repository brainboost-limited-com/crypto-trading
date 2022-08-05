from com_goldenthinker_trade_logger.Logger import Logger
import cherrypy


class GlobalLogger(object):
    
    
    @cherrypy.expose
    def log(self,trade_log,telegram=False,public=False,trace=False):
        Logger.log(trade_log,telegram,public,trace)
    
    
    
    
Logger.set_process_name(name='gt_global_logger')
Logger.log("Logger gateway starting",telegram=True)
cherrypy.config.update({'server.socket_host': '127.0.0.1'})
cherrypy.quickstart(GlobalLogger())
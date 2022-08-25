from com_goldenthinker_trade_logger.Logger import Logger
import cherrypy
import socket


class GlobalLogger(object):
    
    
    @cherrypy.expose
    def log(self,trade_log,pname=None,telegram=False,public=False,trace=False):
        if pname != None and pname != Logger.get_process_name():
            Logger.set_process_name(name=pname+'@'+socket.gethostbyname(socket.gethostname()))
        Logger.log(trade_log,telegram=telegram,public=public,trace=trace,external=False)
    
    
    
    

Logger.log("Logger gateway starting",telegram=True)
cherrypy.config.update({'server.socket_host': '100.96.1.34'})
cherrypy.quickstart(GlobalLogger())
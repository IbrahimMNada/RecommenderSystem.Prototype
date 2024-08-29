
import pypyodbc as pyodbc 


class DatabaseReader:
    def __init__(self, db_host,db_name, db_user,db_password):
        self.connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
    
    def _executeQuery(self,query,param=None):
        db = pyodbc.connect(self.connection_string)
        cursor = db.cursor()
        cursor.execute(query,param)
        query_result = (cursor.description ,cursor.fetchall())
        cursor.close()
        db.close()
        return query_result
    
    def _resultToDict(self,query_result):
        final_result = [dict(zip([column[0] for column in query_result[0]], row)) for row in query_result[1]]
        return final_result

    def GetAllUsers(self):
        queryResult = self._executeQuery(' select * from Users ')
        return self._resultToDict(queryResult)
              
    def GetAllPosts(self):
        queryResult = self._executeQuery(' select Id as post_id , title  from Posts ')
        return self._resultToDict(queryResult)
    
    def GetAllPostViews(self):
        queryResult = self._executeQuery(' select userid as [user_id] , Postid as post_id , intrest   from [dbo].[PostViews] ')
        return self._resultToDict(queryResult)
  
    def GetPostCategory(self,postId):
        queryResult = self._executeQuery(' select Category from posts where id = ? ' , (postId,))
        return self._resultToDict(queryResult)
    
    def GetIntrestsWithPosts(self):
        queryResult = self._executeQuery(' select * from [Posts] p join PostViews pv on p.id = pv.postId ')
        return self._resultToDict(queryResult)

    
    def GetRateingLimits(self):
        queryResult = self._executeQuery(' select min(intrest) As MinIntrest  , max(intrest) As MaxIntrest  from PostViews ')
        return self._resultToDict(queryResult)[0]
    
    def GetPostsNotViewedByUser(self,userId):
        queryResult = self._executeQuery(' select * from [Posts] p join PostViews pv on p.id = pv.postId where Userid <>  ?' , (userId,))
        return self._resultToDict(queryResult)
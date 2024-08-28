
import pypyodbc as pyodbc 


class DatabaseReader:
    def __init__(self, db_host,db_name, db_user,db_password):
        self.connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
    

    def GetAllUsers(self):
        db = pyodbc.connect(self.connection_string)
        SQL = ' select id as user_id , * from Users '
        cursor = db.cursor()
        cursor.execute(SQL)
        query_results = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        cursor.close()
        db.close()
        return query_results
        
        
    def GetAllPosts(self):
        db = pyodbc.connect(self.connection_string)
        SQL = ' select Id as post_id , title  from Posts '
        cursor = db.cursor()
        cursor.execute(SQL)
        query_results = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        cursor.close()
        db.close()
        return query_results
    
    def GetAllPostViews(self):
        db = pyodbc.connect(self.connection_string)
        SQL = ' select userid as [user_id] , Postid as post_id , intrest   from [dbo].[PostViews] '
        cursor = db.cursor()
        cursor.execute(SQL)
        query_results = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        cursor.close()
        db.close()
        return query_results
    
    
    def GetPostCategory(self,postId):
        db = pyodbc.connect(self.connection_string)
        SQL = ' select Category from posts where id =  ' + str(postId)
        cursor = db.cursor()
        cursor.execute(SQL)
        query_results = cursor.fetchone()
        cursor.close()
        db.close()
        return query_results
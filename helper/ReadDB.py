import awswrangler as wr

class ReadDB:
    """
    class : Read Database from AWS RDS
    """
    def __init__(self, db='postgresql'):
        self.db = db

        try:
            if self.db == 'postgresql':
                self.db = wr.postgresql
                self.con = self.db.connect("crawler_1")
            elif self.db == 'MS':
                self.db = wr.sqlserver
                self.con = self.db.connect("crawler_2")
            else:
                assert False

        except AssertionError as e:
            print(f"Invalid Type of db \'{db}\' \n Insert one 'postgresql' OR 'MS'")

    def read_query(self, query):
        self.query = query
        self.data = self.db.read_sql_query(self.query, self.con)
        self.con.close()

        return self.data

if __name__ == "__main__" :
   postgresql = ReadDB()
   query = 'select count(*) from source.yl_bas0800'
   test = postgresql.read_query(query)
   print(test)
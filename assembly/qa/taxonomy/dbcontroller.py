import sqlite3

class DbController:
    def __init__(self, dbFilepath):

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        self.dbFilepath = dbFilepath
        self.con = sqlite3.connect(self.dbFilepath)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()

    def __del__(self):
        self.con.close()

    def execute(self, query, arg=None):
        try:
            if arg is None:
                self.cur.execute(query)
            else:
                self.cur.execute(query, arg)
            self.con.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
            print(e)
            return False
        return True
    
    def __accession2taxid(self, accessionVersion):
        query = 'SELECT taxid FROM accession2taxid WHERE accession_version = "{}"'.format(accessionVersion)
        success = self.execute(query)
        if success:
            ret=self.cur.fetchone()
            if ret is not None:
                return ret["taxid"]
        return None
        
    def accession2taxid(self, accessionVersion_lst):
        taxid_lst=[]
        for accessionVersion in accessionVersion_lst:
            result = self.__accession2taxid(accessionVersion)
            if result is not None:
                taxid_lst.append(result)
            else:
                taxid_lst.append(0)
        assert len(taxid_lst)==len(accessionVersion_lst)
        return taxid_lst
    
if __name__=='__main__':
    dc = DbController("/work/GoryaninU/mitsuki/blast/accession2taxid/prot.accession2taxid.db")
    print(dc.accession2taxid(["WP_091645391.1", "hoge", "WP_096446619.1"]))
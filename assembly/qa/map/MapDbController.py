from myutil.myutil import DbController

class MapDbController(DbController):
    
    def __init__(self, dbFilepath):
        super().__init__(dbFilepath)

    def calc_mappability(self, table, length):
        assert table in ("bowtie", "bwa")
        assert isinstance(length, int)
        
        query = ("SELECT COUNT(DISTINCT read_id) as count FROM {0} " \
                +"WHERE scaff_id in ( " \
                +"SELECT id FROM scaffold WHERE length >= {1})").format(table, length)
        success = self.execute(query)
        if success:
            return self.cur.fetchone()["count"]
        else:
            return None
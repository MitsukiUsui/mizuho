### exec
1. `./pipeline_map.sh`
* align reads to scaffolds and get sam
1. `./pipeline_db.sh`
* based on the sam, summarize information into db (sqlite3)
1. `./pipeline_stat.sh`
* query various mapping information to the db

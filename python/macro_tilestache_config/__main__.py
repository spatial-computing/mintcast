#!/usr/bin/env python3

import sys, json, os, psycopg2, pymongo
import psycopg2.extras
import os.path

MINTCAST_PATH = os.environ.get('MINTCAST_PATH')
config_path = MINTCAST_PATH + "/config/"
TILESTACHE_CONFIG_PATH = os.environ.get('TILESTACHE_CONFIG_PATH')
sys.path.append(config_path)

from postgres_config import hostname, username, password, database, MONGODB_CONNECTION

#DATABASE_PATH = '/sql/database.sqlite'
MINTY_SERVER_URL = "http://minty.mintviz.org/"

mongo_client = pymongo.MongoClient(MONGODB_CONNECTION) # defaults to port 27017
mongo_db = mongo_client["mintcast"]
mongo_metadata = mongo_db["metadata"]

def main(base_dir="/data", enable_mongo=True):
    config = {
      "type": "tilestache-config",
      "index": MINTY_SERVER_URL + "minty/tilestache/index.html",
      "cache": {
        "name": "Redis",
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "key prefix": "tilestache",
      },
      "layers": {
      }
    }

    #conn = sqlite3.connect(MINTCAST_PATH + DATABASE_PATH)
    #from postgres_config import conn
    conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        c.execute('SELECT * FROM mintcast.tileserverconfig where layer_name in (select name from mintcast.layer) or layer_name = \'\'')
        for row in c.fetchall():
            tileset_path = None
            if row['mbtiles'][0] == '.':
                tileset_path = base_dir + row['mbtiles'].lstrip('.')
            elif row['mbtiles'].startswith(base_dir) and os.path.isfile(row['mbtiles']):
                tileset_path = row['mbtiles']
            else:
                tileset_path = base_dir + row['mbtiles']
            tileset_path = tileset_path.replace('//','/')
            config['layers'][row['md5']] = {
                      "provider": {
                        "name": "mbtiles", 
                        "tileset": tileset_path
                      },
                      "allowed origin": "*",
                      "cache lifespan": "604800"
                }
            if row['layerid'].find('vector_pbf') != -1 :
                config['layers'][row['md5']]["content encoding"] = "gzip"
            # elif row['layerid'].find('raster_png') != -1:
            #     pass
        # print(jsonStr)
        if enable_mongo:
            ftmp = mongo_metadata.find_one({'type': 'tilestache-config'})
            if ftmp:
                mongo_metadata.update_one({'type': 'tilestache-config'}, { '$set': config })
            else:
                mongo_metadata.insert_one(config)
        jsonStr = json.dumps(config, indent=4)
        f = open(TILESTACHE_CONFIG_PATH + "/tilestache.json",'w')
        f.write(jsonStr)
        f.close()
        print('Write into tilestache.json Done')
    except Exception as e:
        raise e
    finally:
        conn.close()

usage = '''
USAGE:
    main.py root
    main.py root disable-mongo
'''
if __name__ == '__main__':
    num_args = len(sys.argv)
    if not TILESTACHE_CONFIG_PATH:
        print("Please set TILESTACHE_CONFIG_PATH first", file=sys.stderr)
        exit(1)
    if num_args == 2:
        main(sys.argv[1])
    elif num_args == 3:
        main(sys.argv[1], False if sys.argv[1].lower() not in {'no','0','neg'} else True)
    else:
        print(usage, file=sys.stderr)
        exit(1)
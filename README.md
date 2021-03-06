# Automated Script

![Directed by Yaoyi Chiang](https://img.shields.io/badge/Yaoyi%20Chiang-Director-blue.svg)
![Published by Libo Liu](https://img.shields.io/badge/Libo%20Liu-Author-blue.svg)
![Published by Adam Vaccaro](https://img.shields.io/badge/Adam%20Vaccaro-Author-blue.svg)


### Config/postgres_config.py

```
#!/usr/bin/env python3

import sys, os, psycopg2

MINTCAST_PATH = os.environ.get('MINTCAST_PATH')

hostname = ''
username = ''
password = ''
database = ''
```

## TODO List:
- Fix json problem √
- Add shapefile √
- Timeseries Json file
	- with hotspot geojson object
	- with a series data loading 
	- time slide desc data
- Consistence √
	- filename √
	- only use Json file instead of `metadata.json` √
	- timeseries source-layer √
	- layer name and source name, make them consistent √
- Timeseries Play √
	- frame request √
	- play/pause button √
	- slide bar redesign 
- Postgres
	- No show all √
	- Add one flag if it changed
		- `0` not changed
		- `1` changing
		- `2` changed
	- New structure √
		- no metadata.json √
		- only seperate files √
		- md5 file √
	- Search without metadata.json √
		- Search using redis √
		- Search via AJAX √
		- redis: name: md5 √
	- Increment 
		- Postgresql with timeseries flag => md5
		- Generate into the same json file with the same timeseries flag
		- **each file is one seperated record**
- the reason still using Json file not DB √
	- faster to send the response √
	- more secure √
	- without connect and join tables √
	- Json file structure √
		- move `metadata.json` to seperated json files √
- Hotspot data generating
	- Geojson object 
	- store data into Postgresql for each file
	- when generate json file merge them into one geojson object
- Map
	- a new variable to fly to a new area 
	- remove metadata.json √
	- remove `show all dataset` √
	- move search to redis  √
	
### Tileserver Selection

[Ref](http://www.paulnorman.ca/blog/2016/11/serving-vector-tiles/)

|Server|Full planet|Diff updates|Non-OSM data|GeoJSON|TopoJSON|Mapbox Vector Tiles|
|--- |--- |--- |--- |--- |--- |--- |
|node-mapnik|Yes|Yes|Yes|Some|No|Yes|
|Tilezen tileserver|Yes|Yes|Yes|Yes|Yes|Yes|
|Tegola|Yes|Yes|Yes|No|No|Yes|
|t-rex|Yes|Yes|Yes|No|No|Yes|
|TileStache|Yes|Yes|Yes|Yes|No|Yes|
|Tilemaker|No|No|Yes|No|No|Yes|
|VectorTileCreator|Unknown|No|No|No|No|No|

## Time series convention

### How time series stored in `metadata.json`
```
	"layerNames": [
        "Evap"
    ],
    "layerIds": [
        "evap_vector_pbf"
    ],
    "sourceLayers": [
        "evap"
    ],
    "hasData": [
        true
    ],
    "hasTimeline": [
        true
    ],
    "vectorMD5":[
        null
    ],
    "rasterMD5":[
        null
    ],
    "layers": [
        {
            "id": "evap_vector_pbf",
            "source-layer": "evap",
            "minzoom": 14,
            "maxzoom": 3,
            "type": "vector",

            "dataset": "Elevation",
            "axis":"slider",
            "stepOption":{"name":"Time","type":"string|unix", "format":"yyyyMMdd", },
            "step":[],
            "vectormd5":["59feb8015325307ba6e75078519c424a","xxx"],
            "rasterMD5":["x","xxx"]
        },
```
### How time series stored in `config.json`

```
	"data": {
        "59feb8015325307ba6e75078519c424a": {
            "mbtiles": "./dist/{dataset}/{year}/{month}/whatever-it-is{day}.nc/evap_vector_pbf.mbtiles"
        }
```

## GDAL Version conflict

When install Gdal, flags have to be added to `./configure --with-armadillo --with-complete --with-libkml --with-unsupported`

```shell
brew install jasper netcdf
brew reinstall gdal --with-armadillo --with-complete --with-libkml --with-unsupported
```

## Conventions

- The project name `mintcast`
- All lib scripts should be `function`, will be included using `source lib/xxx.sh`, and call the function `xxx(x1, x2)`
- All names should be in lowercase
- All file should have `shebang line`, like `#!/usr/bin/env bash`  or `#!/usr/bin/env python3`
	- All python scripts will be added executable mod when user run `./install.sh`
	- Thus, there is no difference between python3 or python2.7 scripts when run it.

- Names of `lib` scripts should start with `check_`, `proc_` and `handle_`
	- `check_` like `lib/check_type.sh`, the function inside this file should be `check_type()`
	- `proc_` like `lib/proc_polygonize.sh`, the function should be `proc_polygonize()`
	- `handle_` like `lib/handle_netcdf.sh`, the function should be `handle_netcdf.sh`, 
	- !!!(deperacted) the return value should be `YES\NO` to indicate whether the process is a success. Other return data should be transfered by referenced parameters
	- All functions will be called in `bin/mintcast.sh`
	- Important info should show in different color https://misc.flogisoft.com/bash/tip_colors_and_formatting

- Names of `python` scripts should be `macro_` or `handle_` like `python/handle_grid_csv/__main__.py` or `python/macro_extract_lnglat/__main__.py`
	- Python script should get paramter from `promot`
	- Python script should output every thing in `stdout`
	- Python script should show process message in `stderr` in a different colors as bash



## MySQL

```sh
mysql -umint -pyOuaReAgeNius -h 13.57.22.75 mintmap
```

## Shell

### If there is error, stop the shell

### Library

- lib/
    - shell function
- python/
    - python script to handle 

### Handle parameters

- -qml

- -type

	- nc

	- tiff

	- tiled

- -dir

	- Use for time series

	- Use for tiled

		- -dir aaa/\*.zip

- -start-time

- -end-time

- -layer-name

### Extract file info 

- Store to MySQL

- Use as condition to run procedure

### Decide which type file it is

- Tiff

- Tiff with QML

	- Detect whether dataset is Byte format/if not convert

	- Clip use shapefile

	- Detect/To EPSG 3857

	- Python to handle QML

		- Generate color.txt

		- Write to database

	- Generate Raster Tile

		- -tr 10 10 (Resolution to keep the cell)

		- Render color.txt on tiff

			- Question: How to render linear gradient to tif ?(0% #000. 100% #fff)?

		- Translate tif to mbtiles

		- gdaladdo mbtiles generate different levels

		- Read mbtiles’ metadata table, store data to database

	- Generate Vector Tile

		- Polygonize to geojson

		- Get the layer name from parameter

			- Layer name from parameter

			- If there are multiple file(like netcdf), use the name of subdataset

			- Property name would be always `value`

		- Tippecanoe geojson to mbtiles

		- Read mbtiles’ metadata table, store data to database

		- Generate dataset.json file for vector tile

	- Update website’s config.json

	- Copy all mbtiles files to a location

		- Mbtile To dist/

		- Json to dist/json

		- Intermediate file to tmp/

		- All in .gitignore

	- Delete all mediate files

- NetCDF

	- Timeseries

		- Pass dir name

		- Start time and end time

	- Read NetCDF get all subdatasets

	- Proceed as Tiff with QML

	- When generate vector mbtiles, try to merge all layer in one for oneday

	- Store the time series in database

- Tiled

	- Detect & unzip all files

	- Merge files to tif

	- Proceed as Tiff (with QML)

### Use Python to handle String/Text/Calculation

- QML

	- To colormap

	- To database

- Handle the result of gdal_info

	- To database

	- return value

## TODO

### Use TileStache

### Time series

### Two layer (raster and vector)

### BugToFix

- Multiple legend

- Show all

- csv

- Click after remove layers

## Database

### Design of database

- metadata

	- key

		- server

		- Tile format

		- Config file location

		- Mbtile location

		- metajson file location

		- borderFeatures

			- {  
			        "type": "FeatureCollection",  
			        "features": [  
			          {  
			            "type": "Feature",  
			            "properties": {  
			              "stroke": "#000000",  
			              "stroke-width": 3,  
			              "stroke-opacity": 1,  
			              "fill": "#555555",  
			              "fill-opacity": 0.3  
			            },  
			            "geometry": {  
			              "type": "Polygon",  
			              "coordinates": []  
			            }  
			          }  
			        ]  
			      }

	- value

- layer

	- layerid

	- type

	- name

	- sourceLayer

	- hasData

	- originalDatasetBounds

	- maxzoom

	- minzoom

	- Bounds

	- hasTimeline

	- mbfilename

	- DirectoryFormat:string

		- like {year}/{month}/{day}/{name}.mbtiles

	- starttime

	- endtime

	- jsonfile

	- server

	- styleType

	- original_id

	- Colormap

	- legendType

	- legend

	- valuesArray

	- originalDatasetCoordinate

	- mapping

	- defaultColor

- original

	- Dataset name

	- Filename

	- Filepath

		-  realtive to South_Sudan

			- Like South_Sudan/Rawdata/Soil/xxx/xx.tif

	- gdalinfo:text

	- Related Json

		- convert from xml or other to json

### Use Python to read

- Generate metadata.json (will update the website)

- Generate \*.json for each dataset 

	- Legend

	- Map render

- Generate configuration(tileserver-gl and TileStache)

### Store json in filesystem (in case can is failed)

### Write to ckan

## Website

### Metadata.json

### Dataset.json

### New function: Two layer (raster and vector)

### New function: Time series


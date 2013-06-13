bixml2csv
=====

Transform Bixi's `bikeStations.xml` into CSV

(This also works for other bikeshare systems using Public Bike System Company
equipment.)


Installation
------------

Eventually this will be packaged and put in PyPI. For now, clone this repository
and install the dependencies with `pip -r requirements.txt`.


Usage
-----

```
usage: parse.py [-h] [-v] [--header] [file]

positional arguments:
  file           file or directory to process

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  be verbose (specify twice for more)
  --header       print column header row
```

`file` can be a file or a directory; if it's a directory then the script walks
it attempting to process any files with a .xml extension.  If it's a file with
.tar extension, then it attempts to read it as a tar archive and process all
files with .xml extension found within. Otherwise it assumes it a single XML
file.

Example
-------

Try it out with Bixi's current data:

```
$ curl -s https://montreal.bixi.com/data/bikeStations.xml > bikeStations.xml
$ python parse.py --header bikeStations.xml | head -5
lastUpdate,id,latestUpdateTime,name,terminalName,lat,long,installed,locked,installDate,removalDate,temporary,nbBikes,nbEmptyDocks
1371137358194,1,1371136838594,"Notre Dame / Place Jacques
Cartier",6001,45.508183,-73.554094,true,false,1366905720000,1353352920000,false,5,22
1371137358194,2,1371136805367,Dézery/Ste-Catherine,6002,45.5392,-73.5414,true,false,1365877320000,1353638460000,false,2,21
1371137358194,4,1371136331092,"Berri /
Saint-Antoine",6004,45.51205360327094,-73.55393081903458,true,false,1364404740000,1353352920000,false,15,18
1371137358194,6,1371133964174,"Saint-Antoine / de
l'Hôtel-de-Ville",6006,45.50875,-73.55613,true,false,1364400360000,1353359340000,false,10,5
[Errno 32] Broken pipe
```

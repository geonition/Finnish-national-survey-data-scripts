#!/bin/bash

for zipfile in *.zip
do
  echo "Processing $zipfile"
  leaf=${zipfile%%[.]*}
  echo "Leaf $leaf"
  unzip $zipfile

  for shapefile in *.shp
  do
    echo "shapefile $shapefile"
    tablename=${shapefile/xxxxxx/$leaf}
    tablename=${tablename/.shp/}
    echo "table name $tablename"
    shp2pgsql -d -D -s 3067 -i -I $shapefile $tablename > $shapefile.sql
    psql -U ksnabb -h 176.34.103.100 -d mml -f $shapefile.sql
  done

  rm *.shp
  rm *.dbf
  rm *.shx
  rm *.prj
  rm *.sql
done

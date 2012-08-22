import os
import zipfile
from glob import glob
import re		

tablenames = ['%s%s' % (t, gt) for t in ['l','j','m','n','r','k','s','e','h','u'] for gt in ['v','s','t','p']]

for tablename in tablenames:
    first_char = tablename[0]
    last_char = tablename[-1]
    
    file_list = os.listdir('.')
    
    zip_files = []
    for f in file_list:
        if f.endswith('.zip'):
            zip_files.append(f)
    
    table_created = False
    
    for zf in zip_files:
        leaf = zf.split('.')[0]
        leaf_pattern = '^%s' % tablename[1:-1]
    
        if re.match(leaf_pattern, zf):
            print leaf
        else:
            continue
        
        zipfile.ZipFile(zf).extractall()
        
        for shp in glob('*.shp'):
            shape_pattern = '%s......%s.shp' % (first_char, last_char)
            if re.match(shape_pattern, shp):
                if not table_created:    
                    os.system('shp2pgsql -d -W "latin1" -D -s 3067 -i -I %s %s > %s.sql' % (shp,
                                                                                tablename,
                                                                                tablename))
                    os.system('psql -U ksnabb -h 176.34.103.100 -d mml -f %s.sql' % tablename)
                    
                    table_created = True
                else:    
                    os.system('shp2pgsql -a -W "latin1" -D -s 3067 -i %s %s > %s.sql' % (shp,
                                                                             tablename,
                                                                             tablename))
                    os.system('psql -U ksnabb -h 176.34.103.100 -d mml -f %s.sql' % tablename)
    
        for gf in glob('*.shp'):
            os.remove(gf)
        for gf in glob('*.dbf'):
            os.remove(gf)
        for gf in glob('*.shx'):
            os.remove(gf)
        for gf in glob('*.prj'):
            os.remove(gf)
        for gf in glob('*.sql'):
            os.remove(gf)
            
#print out the CLUSTER SQL commands
for tablename in tablenames:
    
    print 'CLUSTER %s USING %s_the_geom_gist;' % (tablename, tablename)
    
#remember to VACUUM
print 'VACUUM FULL;'
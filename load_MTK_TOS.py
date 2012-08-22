import os
import zipfile
from glob import glob
import re		

tablenames = ['%s%s' % (t, gt) for t in ['u'] for gt in ['v','s','t','p']]

for tablename in tablenames:
    first_char = tablename[0]
    last_char = tablename[-1]
    
    file_list = os.listdir('./MTK_TOS')
    
    zip_files = []
    for f in file_list:
        if f.endswith('.zip'):
            zip_files.append(f)
    
    table_created = False
    
    for zf in zip_files:
        zipfile.ZipFile('MTK_TOS/%s' % zf).extractall('./MTK_TOS')
        
        for shp in glob('MTK_TOS/*.shp'):
            shape_pattern = '^MTK_TOS/%s......%s.shp' % (first_char, last_char)
            if re.match(shape_pattern, shp):
                if not table_created:    
                    os.system('shp2pgsql -d -W "latin1" -D -s 3067 -i -I %s %s%s > %s%s.sql' % (shp,
                                                                                                'MTK_TOS_',
                                                                                                tablename,
                                                                                                'MTK_TOS_',
                                                                                                tablename))
                    os.system('psql -U ksnabb -h 176.34.103.100 -d mml -f %s%s.sql' % ('MTK_TOS_', tablename))
                    
                    table_created = True
                else:    
                    os.system('shp2pgsql -a -W "latin1" -D -s 3067 -i %s %s%s > %s%s.sql' % (shp,
                                                                                        'MTK_TOS_',
                                                                                        tablename,
                                                                                        'MTK_TOS_',
                                                                                        tablename))
                    os.system('psql -U ksnabb -h 176.34.103.100 -d mml -f %s%s.sql' % ('MTK_TOS_', tablename))
    
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
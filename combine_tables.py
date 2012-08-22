import psycopg2

#merge these tables to one
table_like = 'kk_____v'
new_tablename = 'kkv'
geometry_type = 'MULTILINESTRING'

#connect to database
conn = psycopg2.connect("dbname='mml' user='ksnabb' host=176.34.103.100 password=''")

#query the tablenames
tablename_cur = conn.cursor()
tablename_cur.execute("SELECT tablename FROM pg_tables WHERE tablename LIKE '%s'" % table_like)

rows = tablename_cur.fetchall()
union_select = ""
for row in rows:
    #build union query
    select_query = "(SELECT * FROM %s)" % row[0]
    if union_select != "":
        union_select = "%s UNION %s" % (union_select, select_query) 
    else:
        union_select = "%s" % select_query

tablename_cur.close()
conn.close()

drop_table = "DROP TABLE IF EXISTS %s;" % new_tablename
print drop_table

create_table = """CREATE TABLE %s
(
  gid serial NOT NULL,
  teksti character varying(80),
  ryhma double precision,
  luokka double precision,
  tastar double precision,
  kortar double precision,
  korarv double precision,
  kulkutapa double precision,
  kohdeoso double precision,
  ainlahde double precision,
  syntyhetki character varying(8),
  kuolhetki character varying(8),
  kartoglk double precision,
  aluejakoon double precision,
  versuh double precision,
  suunta double precision,
  siirt_dx double precision,
  siirt_dy double precision,
  korkeus double precision,
  attr2 double precision,
  attr3 double precision,
  the_geom geometry,
  CONSTRAINT %s_pkey PRIMARY KEY (gid ),
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
  CONSTRAINT enforce_geotype_the_geom CHECK (geometrytype(the_geom) = '%s'::text OR the_geom IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 3067)
)
WITH (
  OIDS=FALSE
);""" % (new_tablename,
        new_tablename,
        geometry_type)

print create_table

alter_table = """
ALTER TABLE %s
  OWNER TO ksnabb;""" % new_tablename

print alter_table

alter_table = """
GRANT SELECT ON TABLE %s TO public;""" % new_tablename
print alter_table

alter_table = """
GRANT ALL ON TABLE %s TO ksnabb;
""" % new_tablename
print alter_table

alter_table = """
DROP INDEX IF EXISTS %s_the_geom_gist;
""" % new_tablename
print alter_table

alter_table = """
CREATE INDEX %s_the_geom_gist
  ON %s
  USING gist
  (the_geom );""" % (new_tablename,
                    new_tablename)

print alter_table


insert_select = """
INSERT INTO %s (
teksti,
ryhma,
luokka,
tastar,
kortar,
korarv,
kulkutapa,
kohdeoso,
ainlahde,
syntyhetki,
kuolhetki,
kartoglk,
aluejakoon,
versuh,
siirt_dx,
siirt_dy,
korkeus,
attr2,
attr3,
the_geom)

SELECT 
teksti,
ryhma,
luokka,
tastar,
kortar,
korarv,
kulkutapa,
kohdeoso,
ainlahde,
syntyhetki,
kuolhetki,
kartoglk,
aluejakoon,
versuh,
siirt_dx,
siirt_dy,
korkeus,
attr2,
attr3,
the_geom
FROM (%s) AS data;""" % (new_tablename, union_select)

print insert_select
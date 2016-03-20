# postgis-geosjon

*This is a half-baked implementation of a half-baked idea. It's awesome but don't use it yet*

## Goal

A command line interface to use Postgres as a document store for GeoJSON features.
**P**ost**G**is**G**eo**J**SON stores geojson features in postgres but doesn't try to model the properties as a schema. Instead

  * geometry as postgis GEOMETRY column (assumed 4326)
  * properties as a JSONB column

Every valid GeoJSON feature therefore fits into a single table schema. You can use the
wonders of JSONB to query it.

The command line matches the semantics of SQL with `INSERT`, `CREATE` and `SELECT` subcommands.

## Example

Words, words, words. Here it is in action::

Create a postgis database (I'm using postgis 2.2 and postgres 9.5)
```
$ export POSTGIS_GEOJSON_DB="postgres://user:password@localhost:5432/geojsondb"
$ createdb geojsondb
$ psql $POSTGIS_GEOJSON_DB
geojsondb=# CREATE EXTENSION postgis;
geojsondb=# \q
```

`CREATE` a table to hold your features
```
$ pggj create myfeatures
```

`INSERT` some features
```
$ pggj insert dataset.geojson myfeatures          # feature collection
$ fio cat dataset.shp | pggj insert myfeatures    # or features on stdin
```

`SELECT` features using [JSON functions](http://www.postgresql.org/docs/9.5/static/functions-json.html) to access properties.
```
$ pggj select myfeatures --where "properties->>'region_wb' ~ 'Africa'"
# .... line-delimited features on stdout .....
```

## TODO
so much....

* transactions
* async
* indexes
* connection pooling
* avoid hacky sql string construction
* rs, collections, and other output options
* setup, pypi, tests, docs

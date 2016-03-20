# postgres-geosjon

*This is a half-baked implementation of a half-baked idea. It's awesome but don't use it yet*

## Goal

A document store for GeoJSON features?  A spatial NoSQL/SQL hybrid? Call it what you will. 

Store geojson features in postgres but don't try to model the properties as a schema

  * geometry as postgis GEOMETRY column (assumed 4326)
  * properties as a JSONB column

Every valid GeoJSON feature therefore fits into a single schema. 

The command line matches the semantics of SQL with `INSERT`, `CREATE` and `SELECT` subcommands.

## Example

Words, words, words. Here it is in action::

Create a postgis database (I'm using postgis 2.2 and postgres 9.5)
```
$ export DB="postgres://user:password@localhost:5432/geojsondb"
$ createdb geojsondb
$ psql $DB
# CREATE EXTENSION postgis;
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
# .... line-deliminted features on stdout .....
```

## TODO
so much....

* transactions
* async
* indexes
* connection pooling
* db as env var
* tablename as variable
* no hacky where strings
* rs, collections, and other output options
* setup, pypi, tests, docs

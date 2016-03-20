#!/usr/bin/env python
import json

import click
import cligj
from shapely.geometry import asShape
import psycopg2


db_arg = click.option("--db", envvar='POSTGIS_GEOJSON_DB')
where_opt = click.option("--where", required=False, default=None)
table_arg = click.argument("table")


@click.group()
def pggj():
    pass


@pggj.command(help="Insert features into postgis table")
@db_arg
@cligj.features_in_arg
@table_arg
def insert(db, table, features):
    with psycopg2.connect(db) as conn:
        with conn.cursor() as cur:
            for feature in features:
                query = """
                    INSERT INTO {} (id, properties, geometry)
                    VALUES (%s, %s, ST_GeomFromText(%s, 4326))""".format(table)
                try:
                    fid = feature['id']
                except KeyError:
                    fid = None
                cur.execute(
                    query,
                    (fid,
                     json.dumps(feature['properties']),
                     asShape(feature['geometry']).wkt))


@pggj.command(help="Select features from postgis")
@db_arg
@table_arg
@where_opt
def select(db, table, where):
    with psycopg2.connect(db) as conn:
        with conn.cursor() as cur:
            query = """
                SELECT id, properties, ST_AsGeoJSON(geometry, 9)
                FROM {}""".format(table)
            if where:
                # HOLY SHIT, WTF DONT DO THIS, ARE YOU ON CRACK?
                query += " WHERE {}".format(where)

            cur.execute(query)
            for row in cur:
                fid = row[0]
                properties = row[1]
                geom = json.loads(row[2])  # load then dump is wasteful but :shruggie:
                feat = {
                    'type': "Feature",
                    'properties': properties,
                    'geometry': geom}
                if fid:
                    feat['id'] = fid

                click.echo(json.dumps(feat))


@pggj.command(help="Create features table")
@db_arg
@table_arg
def create(db, table):
    with psycopg2.connect(db) as conn:
        with conn.cursor() as cur:
            query = """
                CREATE TABLE {} (
                    id varchar,
                    properties jsonb,
                    geometry geometry(GEOMETRY,4326))""".format(table)
            cur.execute(query)


if __name__ == "__main__":
    pggj()

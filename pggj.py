#!/usr/bin/env python
import json

import click
import cligj
from shapely.geometry import asShape, mapping
from shapely.wkb import loads
import psycopg2


uri_arg = click.argument("uri", required=True)
where_opt = click.option("--where", required=False, default=None)
table_arg = click.argument("table")


@click.group()
def pggj():
    pass


@pggj.command(help="Select postgis")
@uri_arg
@table_arg
@cligj.features_in_arg
def insert(uri, table, features):
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            for feature in features:
                query = """
                    INSERT INTO test (id, properties, geometry)
                    VALUES (%s, %s, ST_GeomFromText(%s, 4326))"""
                try:
                    fid = feature['id']
                except KeyError:
                    fid = None
                result = cur.execute(
                    query,
                    (fid,
                     json.dumps(feature['properties']),
                     asShape(feature['geometry']).wkt))


@pggj.command(help="Select postgis")
@uri_arg
@table_arg
@where_opt
def select(uri, table, where):
    """
    pggj.py select $db test --where "properties->>'region_wb' ~ 'Africa'"
    """
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            query = "SELECT id, properties, ST_AsGeoJSON(geometry, 9) FROM test"
            if where:
                # HOLY SHIT, WTF DONT DO THIS, ARE YOU ON CRACK?
                query += " WHERE " + where

            cur.execute(query, {'table': table})
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
@uri_arg
@table_arg
def create(uri, table):
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            query = """
                CREATE TABLE test (
                    id varchar,
                    properties jsonb,
                    geometry geometry(GEOMETRY,4326))"""
            cur.execute(query)


if __name__ == "__main__":
    pggj()

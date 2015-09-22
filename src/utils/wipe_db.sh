#!/bin/bash

dropdb -U postgres stonedb
createdb -U postgres stonedb
psql -U postgres stonedb < ../sql/schema.sql

#!/usr/bin/env bash
DB = "biomio_db";
DUMPFILE = "./biomio_dump.sql";
echo "Importing data to $DB from $DUMPFILE";
mysql -ubiomio_gate -pgate -h localhost -e "$DB < $DUMPFILE";

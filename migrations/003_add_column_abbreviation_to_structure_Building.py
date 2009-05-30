from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('structure', 'building', 'abbreviation', 'varchar(20) NOT NULL')

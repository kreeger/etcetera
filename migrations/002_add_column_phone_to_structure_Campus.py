from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('structure', 'campus', 'phone', 'varchar(20) NOT NULL')

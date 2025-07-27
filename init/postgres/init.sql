CREATE USER app_map_my_world WITH PASSWORD '7slm59JUebyYZQ625vUJ';
CREATE DATABASE map_my_world_db ENCODING 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';

GRANT ALL PRIVILEGES ON DATABASE map_my_world_db TO app_map_my_world;
ALTER USER app_map_my_world SUPERUSER;

CREATE USER test_map_my_world WITH PASSWORD 'MRc1VKa5aA0Z';
CREATE DATABASE map_my_world_testdb ENCODING 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';

GRANT ALL PRIVILEGES ON DATABASE map_my_world_testdb TO test_map_my_world;
ALTER USER test_map_my_world SUPERUSER;
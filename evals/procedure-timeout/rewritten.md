sqlpipe stops with `dial tcp: i/o timeout` when it cannot connect to Postgres.

1. If sqlpipe hangs or fails with `dial tcp: i/o timeout`, make sure the host that runs sqlpipe can reach the Postgres port (usually 5432). A security group or firewall rule often blocks the connection.
2. If the database is managed (RDS, Cloud SQL), make sure the instance accepts connections from the IP of sqlpipe.

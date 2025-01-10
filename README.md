# Migrator Tool

A Python-based tool for migrating SQLite `.csdb` files to MySQL, featuring a user-friendly GUI.

## Features
- Easy migration from SQLite to MySQL
- Handles table schemas, constraints, and data
- Supports batch data migration for large tables

## Installation
Install via pip:

```bash
pip install migrator-tool

```
## Extra Details below

### MariaDB Installation and Setup

### Installing MariaDB

MariaDB installation is required unless you have already installed it via XAMPP.

#### On Windows:
1. Download the MariaDB installer from the [official website](https://mariadb.org/download/).
2. Run the installer and follow the setup instructions.
3. During installation, set a root password and remember it for later use.

#### On Linux:
1. Update your package index:
   ```bash
   sudo apt update
   ```
2. Install MariaDB:
   ```bash
   sudo apt install mariadb-server
   ```
3. Start the MariaDB service:
   ```bash
   sudo systemctl start mariadb
   ```
4. Secure the installation:
   ```bash
   sudo mysql_secure_installation
   ```

### Correct Syntax for MariaDB <10.4

For MariaDB versions prior to 10.4, use the following syntax to set the root password:

```sql
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('your_password');
FLUSH PRIVILEGES;
```

### Correct Syntax for MariaDB 10.4+

MariaDB 10.4+ uses a different authentication plugin by default. Update the authentication plugin and password as follows:

1. Set the authentication plugin and password:
   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('your_password');
   SET PASSWORD FOR 'root'@'localhost' = PASSWORD('your_password');
   ```
2. Apply the changes:
   ```sql
   FLUSH PRIVILEGES;
   ```

### Correct Steps for Updating the Plugin

If you connect from `127.0.0.1` or `::1`, update the plugin for these hosts as well:

```sql
ALTER USER 'root'@'127.0.0.1' IDENTIFIED VIA mysql_native_password USING PASSWORD('your_password');
ALTER USER 'root'@'::1' IDENTIFIED VIA mysql_native_password USING PASSWORD('your_password');
```

### Restart the MariaDB Service

After making the changes, restart the MariaDB service to apply the configurations:

#### On Windows:
1. Open the Services Manager (`services.msc`).
2. Locate `MariaDB`.
3. Right-click and select **Restart**.

#### On Linux:
```bash
sudo systemctl restart mariadb
```


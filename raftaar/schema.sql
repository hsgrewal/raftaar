DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS gas;
DROP TABLE IF EXISTS loan;
DROP TABLE IF EXISTS maintenance;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE vehicle (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  owner_id INTEGER NOT NULL,
  vin TEXT NOT NULL,
  license_plate TEXT NOT NULL,
  year TEXT NOT NULL,
  make TEXT NOT NULL,
  model TEXT NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES user (id)
);

CREATE TABLE gas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  vehicle_id INTEGER NOT NULL,
  date TEXT NOT NULL,
  gallons REAL NOT NULL,
  cost REAL NOT NULL,
  mileage INTEGER NOT NULL,
  FOREIGN KEY (vehicle_id) REFERENCES vehicle (id)
);

CREATE TABLE loan (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  vehicle_id INTEGER NOT NULL,
  date TEXT NOT NULL,
  amount REAL NOT NULL,
  cost REAL NOT NULL,
  memo TEXT NOT NULL,
  FOREIGN KEY (vehicle_id) REFERENCES vehicle (id)
);

CREATE TABLE maintenance (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  vehicle_id INTEGER NOT NULL,
  date TEXT NOT NULL,
  cost REAL NOT NULL,
  mileage INTEGER NOT NULL,
  memo TEXT NOT NULL,
  type TEXT NOT NULL,
  FOREIGN KEY (vehicle_id) REFERENCES vehicle (id)
);

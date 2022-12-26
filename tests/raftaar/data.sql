INSERT INTO user (username, password, first_name, last_name)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'Carl', 'Sagan'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 'Grace', 'Hopper');

INSERT INTO vehicle (owner_id, name, vin, license_plate, year, make, model)
VALUES
  (1, 'Raftaar', 'Test VIN', 'Test License Plate', 'Test Year', 'Test Make', 'Test Model'),
  (2, 'Toofaan', 'Test VIN', 'Test License Plate', 'Test Year', 'Test Make', 'Test Model');

INSERT INTO gas (vehicle_id, date, gallons, cost, mileage)
VALUES
  (1, '2022-01-01 07:15:30.123', 9.185, 35.27, 75000);

INSERT INTO maintenance (vehicle_id, date, cost, mileage, memo, type)
VALUES
  (1, '2022-01-01 07:15:30.123', 285.47, 56214, 'Test Maintenance', 'Test Service');

INSERT INTO loan (vehicle_id, date, amount, memo)
VALUES
  (1, '2022-01-01 07:15:30.123', 435.25, 'Test Payment');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');

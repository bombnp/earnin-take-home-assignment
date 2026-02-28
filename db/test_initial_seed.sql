INSERT INTO flights (id, departure_time, arrival_time, departure_airport, arrival_airport, departure_timezone, arrival_timezone)
VALUES
    ('DMK001', '2025-03-10T01:00:00Z', '2025-03-10T04:30:00Z', 'DMK', 'HYD', 'Asia/Bangkok', 'Asia/Bangkok'),
    ('LHR002', '2025-03-10T10:00:00Z', '2025-03-11T05:30:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok'),
    ('JFK003', '2025-03-10T14:00:00Z', '2025-03-10T17:30:00Z', 'JFK', 'LAX', 'America/New_York', 'America/Los_Angeles'),
    ('SIN004', '2025-03-10T23:00:00Z', '2025-03-11T06:30:00Z', 'SIN', 'NRT', 'Asia/Singapore', 'Asia/Tokyo'),
    ('CDG005', '2025-03-10T07:00:00Z', '2025-03-10T09:00:00Z', 'CDG', 'FCO', 'Europe/Paris', 'Europe/Rome')
ON CONFLICT (id) DO NOTHING;

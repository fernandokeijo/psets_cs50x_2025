-- Keep a log of any SQL queries you execute as you solve the mystery.

.schema crime_scene_reports   -- check what's inside that table

--

SELECT description
FROM crime_scene_reports
WHERE day = 28
AND
    month = 7
AND
    street = 'Humphrey Street';             -- seek more information about the case


--

.schema bakery_security_logs              -- check data about the bakery

--

SELECT activity, hour, day FROM bakery_security_logs WHERE day = 28 AND month = 7;       -- verify the entrances and exits from the day (10:28)
--

SELECT transcript FROM interviews WHERE day = 28 AND month = 7 AND year = 2023;                             -- gather nice informations from the interviews

--

SELECT license_plate, hour, minute FROM bakery_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND activity = 'exit'; -- look for the licenses plates by the time that the thief possibily left the place

--

.schema atm_transactions                                           -- check the infos in that table

--

SELECT account_number, id, transaction_type, amount FROM atm_transactions WHERE atm_location = 'Leggett Street' AND day = 28 AND month = 7 AND year = 2023;   -- check the transactions of the day

--

SELECT name, passport_number, license_plate, creation_year FROM people JOIN bank_accounts ON id = person_id WHERE person_id IN (SELECT person_id FROM bank_accounts WHERE account_number IN  (SELECT account_number FROM atm_transactions WHERE atm_location = 'Leggett Street' AND day = 28 AND month = 7 AND year = 2023 AND transaction_type = 'withdraw'));
--get a list of suspects

--

SELECT name, phone_number, passport_number FROM people WHERE name IN (SELECT name FROM people WHERE name = 'Diana' OR name = 'Bruce' OR name = 'Iman' OR name = 'Luca'); -- list infos about the suspects
--

SELECT caller, receiver, duration FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2023 ORDER BY duration ASC; -- look at the calls that lasted less than 1 minute

--

SELECT name, passport_number FROM people WHERE phone_number IN (SELECT phone_number FROM people WHERE phone_number = '(375) 555-8161' OR phone_number = '(725) 555-3243'); -- list more suspects

--

SELECT full_name, city, id FROM airports WHERE city = 'Fiftyville'; -- check the id from the fiftyville airport (8)
--

SELECT hour, minute, destination_airport_id, id FROM flights  WHERE origin_airport_id = 8 AND month = 7 AND day = 29 AND year = 2023 ORDER BY hour ASC, minute ASC; -- flights from the next day

--

SELECT passport_number, seat FROM passengers WHERE flight_id = 36;

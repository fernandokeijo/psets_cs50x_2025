SELECT AVG(rating)
FROM RATINGS
JOIN movies ON movie_id = id WHERE year = 2012;


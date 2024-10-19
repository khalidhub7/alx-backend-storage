-- create table users
SELECT origin, sum(fans) AS nb_fans
FROM metal_bands
-- required: Without it MySQL doesn’t know
-- how to group the data and will throw an error
GROUP BY origin
-- optional
ORDER BY nb_fans DESC;

-- top countries by fan count
SELECT
    origin,
    count(*) nb_fans
FROM
    metal_bands
GROUP BY
    origin
ORDER BY
    nb_fans DESC;

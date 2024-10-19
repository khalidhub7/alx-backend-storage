-- calcule lifespan of the band
-- if it still working use 2022 as it end

SELECT band_name, 
       CASE 
           WHEN formed IS NULL THEN 0
           -- Band still active, use 2022
           WHEN split IS NULL THEN 2022 - formed
           -- Band broke up, use split year
           ELSE split - formed
       END AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;

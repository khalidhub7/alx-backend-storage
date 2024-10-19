-- calcule lifespan of the band
-- if it still working use 2022 as it end
SELECT band_name, 
       CASE 
           WHEN split IS NULL THEN 2022 - YEAR(formed)  -- Band still active, use 2022
           ELSE YEAR(split) - YEAR(formed)              -- Band broke up, use split year
       END AS lifespan
FROM metal_bands
WHERE style = "Glam rock"
ORDER BY lifespan DESC;

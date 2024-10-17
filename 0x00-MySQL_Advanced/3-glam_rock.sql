-- Old school band 
-- SQL script that lists all bands with Glam rock as their main style


SET @this_year := 2022;

SELECT band_name, IF(split IS NULL, @this_year, split) - formed AS lifespan FROM metal_bands WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;

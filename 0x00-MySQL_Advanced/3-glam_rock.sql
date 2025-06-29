-- glam rock bands by lifespan
SELECT
    band_name,
    (IFNULL (split, 2022) - formed) AS lifespan
FROM
    metal_bands
WHERE
    -- → exact match (e.g. only 'Glam rock')
    -- e.g. FIND_IN_SET('Glam rock', 'Heavy metal,Glam rock,Hard rock')
    -- FIND_IN_SET ('Glam rock', REPLACE (style, ', ', ','))
    -- → partial match (e.g. 'Glam rock band')
    style LIKE '%Glam rock%'
    AND formed IS NOT NULL
ORDER BY
    lifespan DESC

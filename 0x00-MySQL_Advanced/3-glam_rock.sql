-- glam rock bands by lifespan
SELECT
    band_name,
    (split - formed) AS lifespan
FROM
    metal_bands
WHERE
    -- e.g. FIND_IN_SET('Glam rock', 'Heavy metal,Glam rock,Hard rock')
    FIND_IN_SET ('Glam rock', REPLACE (style, ', ', ','))
    AND formed IS NOT NULL
ORDER BY
    lifespan DESC

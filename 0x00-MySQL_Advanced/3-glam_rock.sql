-- Script to list all bands with "Glam rock" as their main style, ranked by their longevity.

-- Select band name and compute lifespan based on formed and split year, ordered by lifespan
SELECT band_name, 
    CASE 
        WHEN split IS NOT NULL THEN (split - formed) -- Band has split, use split year
        ELSE (2022 - formed) -- Band has not split, use 2022 for lifespan calculation
    END AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;

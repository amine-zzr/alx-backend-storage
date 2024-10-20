-- Script to list all bands with "Glam rock" as their main style, ranked by their longevity.
-- The output will display the band's name and their lifespan (in years until 2022).
-- Longevity is calculated based on the 'formed' and 'split' year attributes.

SELECT band_name, 
    IFNULL(split, 2022) - formed AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;

-- Script to rank country origins of metal bands by the total number of fans.
-- The output will display the country origin and the total number of fans, ordered by fans in descending order.

-- Select the country origin and sum the number of fans, group by country origin and order by total fans
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

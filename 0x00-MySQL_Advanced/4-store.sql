-- Script to create a trigger that decreases the quantity of an item after a new order is added.
-- The quantity in the 'items' table will be reduced based on the number of items ordered.

-- Drop the trigger if it already exists
DROP TRIGGER IF EXISTS decreases_quantity;

-- Create the trigger for updating item quantity
CREATE TRIGGER decreases_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update the 'items' table to decrease the quantity of the ordered item
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;

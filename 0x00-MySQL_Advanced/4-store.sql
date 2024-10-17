-- Buy buy buy
--  SQL script that creates a trigger (trigger is like instruction that gonna happen each time you insert a row to dev)

CREATE TRIGGER decrease AFTER INSERT ON orders
FOR EACH ROW
    UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;

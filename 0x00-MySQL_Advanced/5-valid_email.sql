-- trigger valid_email column
-- if email is changed
DELEMITER ::

CREATE TRIGGER emailvalid
BEFORE UPDATE ON users
FOR EACH ROW
SET NEW.valid_email = IF(
    NEW.email = OLD.email, NEW.valid_email, 0
    );

::

DELEMITER ;

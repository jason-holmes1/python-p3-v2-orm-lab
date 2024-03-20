from __init__ import CURSOR, CONN
from department import Department
from employee import Employee

class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):

        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )
    @property
    def year(self):
        return self._year
    @year.setter
    def year(self, year):
        if isinstance(year, int) and year >= 2000:
            self._year = year
        else:
            raise ValueError(
                "Year must be a positive integer"
            )
    @property
    def summary(self):
        return self._summary
    @summary.setter
    def summary(self, summary):
        if isinstance(summary, str) and len(summary):
            self._summary = summary
        else:
            raise ValueError(
                "Summary must be a non-empty string"
            )
    @property
    def employee_id(self):
        return self._employee_id
    @employee_id.setter
    def employee_id(self, employee_id):
        if type(employee_id) is int and Employee.find_by_id(employee_id):
            self._employee_id = employee_id
        else:
            raise ValueError(
                "employee_id must reference an employee in the database"
            )
        
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
            """
            values = (self.year, self.summary, self.employee_id)
            CURSOR.execute(sql, values)
            CONN.commit()
            self.id = CURSOR.lastrowid
            Review.all[self.id] = self
        
        

    @classmethod
    def create(cls, year, summary, employee_id):
        #? Initialize a new Review instance and save the object to the database. Return the new instance. """
        review = cls(year, summary, employee_id)
        review.save()
        return review
   
    @classmethod
    def instance_from_db(cls, row=None):
    # Return a Review instance having the attribute values from the table row.
    # Check the dictionary for existing instance using the row's primary key
        if row[0] in cls.all:  # assuming id is the first element in the tuple
            return cls.all[row[0]]
        else:
            return cls(*row)
        
    
   

    @classmethod
    def find_by_id(cls, id):
        #?Return a Review instance having the attribute values from the table row."""
        sql = """
            SELECT * FROM reviews
            WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None
    

    def update(self):
        #?Update the table row corresponding to the current Review instance."""
        sql = """
            UPDATE reviews
            SET year = ?, summary = ?, employee_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()


    def delete(self):
        #?Delete the table row corresponding to the current Review instance,
        #?delete the dictionary entry, and reassign id attribute"""
        sql = """
            DELETE FROM reviews
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None


    @classmethod
    def get_all(cls):
        return list(cls.all.values())

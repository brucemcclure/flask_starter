# 99% of the time you want a model for each table in the db.
from main import db  # db connection


class Example(db.Model):
    __tablename__ = "examples"  # declaring the name of the table in the db
    # The name of the attribute maps to the name of the column on the table

    id = db.Column(db.Integer, primary_key=True)                                    #
    title = db.Column(db.String())                                                  #
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)      #

    def __repr__(self):                                  # Reresentitive state
        return f"<Example {self.title}>"                 # When the Example is printed it now shows the title instead of the id

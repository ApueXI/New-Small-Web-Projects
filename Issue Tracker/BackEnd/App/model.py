from App import db

class Issues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    priority_level = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"No.{self.id}"

    def get_data(self):
        return{
            "id" : self.id,
            "title" : self.title,
            "priority_level" : self.priority_level,
            "details" : self.details,
            "status" : self.status
        }
    
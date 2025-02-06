from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherRecord(db.Model):
    __tablename__ = 'weather_records'
    station_id = db.Column(db.String(50), nullable=False, primary_key=True)
    record_date = db.Column(db.Date, nullable=False, primary_key=True)
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    precipitation = db.Column(db.Float)

    def __repr__(self):
        return f"<WeatherRecord {self.station_id}, {self.record_date}>"

class WeatherStats(db.Model):
    __tablename__ = 'weather_statistics'
    station_id = db.Column(db.String(50), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    avg_max_temp_celsius = db.Column(db.Float)
    avg_min_temp_celsius = db.Column(db.Float)
    total_precipitation_cm = db.Column(db.Float)

    def __repr__(self):
        return f"<WeatherStats {self.station_id}, {self.year}>"

    def to_dict(self):
        return {
            'station_id': self.station_id,
            'year': self.year,
            'avg_max_temp_celsius': self.avg_max_temp_celsius,
            'avg_min_temp_celsius': self.avg_min_temp_celsius,
            'total_precipitation_cm': self.total_precipitation_cm
        }
        
# from flask_sqlalchemy import SQLAlchemy

# # Initialize the database
# db = SQLAlchemy()

# class WeatherRecord(db.Model):
#     __tablename__ = 'weather_records'
    
#     station_id = db.Column(db.String(50), primary_key=True)
#     record_date = db.Column(db.Date, primary_key=True)
#     max_temp = db.Column(db.Float)
#     min_temp = db.Column(db.Float)
#     precipitation = db.Column(db.Float)

#     def __repr__(self):
#         return f"<WeatherRecord {self.station_id}, {self.record_date}>"

# class WeatherStats(db.Model):
#     __tablename__ = 'weather_statistics'
#     __table_args__ = {'schema': 'data_c'}  # Specify the schema here
    
#     station_id = db.Column(db.String(50), primary_key=True)
#     year = db.Column(db.Integer, primary_key=True)
#     avg_max_temp_celsius = db.Column(db.Float)
#     avg_min_temp_celsius = db.Column(db.Float)
#     total_precipitation_cm = db.Column(db.Float)

#     def __repr__(self):
#         return f"<WeatherStats {self.station_id}, {self.year}>"

#     def to_dict(self):
#         return {
#             'station_id': self.station_id,
#             'year': self.year,
#             'avg_max_temp_celsius': self.avg_max_temp_celsius,
#             'avg_min_temp_celsius': self.avg_min_temp_celsius,
#             'total_precipitation_cm': self.total_precipitation_cm
#         }
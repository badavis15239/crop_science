from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from models import db, WeatherRecord, WeatherStats
import yaml

# Initialize Flask app and API
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@0.0.0.0/data'  # Replace with your DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app, doc='/swagger')

# Define the API model for serialization
weather_model = api.model('WeatherModel', {
    'station_id': fields.String,
    'record_date': fields.Date,
    'max_temp': fields.Float,
    'min_temp': fields.Float,
    'precipitation': fields.Float
})

stats_model = api.model('WeatherStatsModel', {
    'station_id': fields.String,
    'year': fields.Integer,
    'avg_max_temp_celsius': fields.Float,
    'avg_min_temp_celsius': fields.Float,
    'total_precipitation_cm': fields.Float
})

# API endpoint for weather records with pagination
@api.route('/api/weather')
class Weather(Resource):
    def get(self):
        # Parse query parameters for filtering
        station_id = request.args.get('station_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = WeatherRecord.query

        if station_id:
            query = query.filter_by(station_id=station_id)
        if start_date:
            query = query.filter(WeatherRecord.record_date >= start_date)
        if end_date:
            query = query.filter(WeatherRecord.record_date <= end_date)

        # Pagination
        records = query.paginate(page=page, per_page=per_page, error_out=False)

        # Serialize records to a list of dictionaries
        data = []
        for record in records.items:
            # Convert each record to a dictionary, excluding internal state
            record_data = {column.name: getattr(record, column.name) for column in record.__table__.columns}
            data.append(record_data)

        return jsonify({
            'data': data,
            'page': page,
            'per_page': per_page,
            'total': records.total
        })



# API endpoint for weather statistics with pagination
@api.route('/api/weather/stats')
class WeatherStatsResource(Resource):
    def get(self):
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)  # Default to page 1
        per_page = request.args.get('per_page', 10, type=int)  # Default to 10 items per page

        # Filter by station_id if provided
        station_id = request.args.get('station_id', None)

        query = WeatherStats.query
        if station_id:
            query = query.filter(WeatherStats.station_id == station_id)

        # Get paginated results
        stats = query.paginate(page=page, per_page=per_page, error_out=False)

        # Prepare result to return (use to_dict if you have it implemented in your model)
        results = [stat.to_dict() for stat in stats.items]  # Assuming to_dict method is implemented

        return jsonify({
            'page': stats.page,
            'per_page': stats.per_page,
            'total': stats.total,
            'total_pages': stats.pages,
            'data': results
        })


# Swagger API documentation
@api.route('/swagger')
class SwaggerDocs(Resource):
    def get(self):
        return jsonify(swagger_spec)

if __name__ == '__main__':
    app.run(debug=True)

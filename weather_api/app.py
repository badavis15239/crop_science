# Assuming you have the following model 'WeatherRecord' with appropriate fields
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import WeatherRecord, WeatherStats
from flask_restx import Api, Resource
from flask_restx import reqparse
import yaml

# Initialize Flask app
app = Flask(__name__)

# Initialize Flask-RESTX API
api = Api(app, doc='/swagger')  # Swagger UI available at /swagger

# # Load the YAML Swagger documentation (Optional if you want to use custom spec)
# with open('swagger.yaml', 'r') as file:
#     swagger_spec = yaml.safe_load(file)

# # Set the spec for Flask-RESTX API (Optional, if you're using a custom spec)
# api.specs = [swagger_spec]  # Use custom spec from swagger.yaml if needed


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/data'
db = SQLAlchemy(app)

@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)  # Default to page 1 if not provided
    per_page = request.args.get('per_page', 10, type=int)  # Default to 10 items per page

    # Query to get the weather statistics from the 'weather_statistics' table
    query = db.session.query(WeatherStats)  # Replace 'WeatherStatistics' with your actual model

    # Apply pagination correctly
    stats = query.paginate(page=page, per_page=per_page, error_out=False)

    # Prepare the response data
    data = {
        'weather_stats': [stat.to_dict() for stat in stats.items],  # Assuming 'to_dict()' method for serialization
        'total': stats.total,
        'pages': stats.pages,
        'current_page': stats.page,
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

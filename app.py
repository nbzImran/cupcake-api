"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import connect_db, db, Cupcake


app = Flask(__name__)


#configure the app to use the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)


with app.app_context():
    db.create_all()


DEFAULT_IMAGE = "https://via.placeholder.com/150"


@app.route('/')
def home_page():
    """render the main cupcake page."""
    return render_template('index.html')



@app.route('/api/cupcakes', methods=["GET"])
def get_all_cupcakes():
    """Get all the cupcakes."""

    cupcakes = Cupcake.query.all()

    Serialized = [
        {
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image
        }
        for cupcake in cupcakes
    ]

    return jsonify(cupcakes=Serialized)



@app.route('/api/cupcakes/<int:cupcake_id>', methods=["GET"])
def get_cupcake(cupcake_id):
    """Get details about a cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    Serialized = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }
    return jsonify(cupcake=Serialized)



@app.route('/api/cupcakes', methods=['POST'])
def creat_cupcake():
    """Create a new cupcake and return its data."""
    
    data = request.json
    print("Recived data:", data)

    missing_fields = [field for field in ["flavor", "size", "rating"] if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"missing fields: {','.join(missing_fields)}"}), 400

    image = data.get("image") or DEFAULT_IMAGE
    #creat a new cupcake instance

    cupcake = Cupcake(
        flavor=data["flavor"],
        size=data["size"],
        rating=data["rating"],
        image=image
    )
    db.session.add(cupcake)
    db.session.commit()

    Serialized = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }
    return jsonify(cupcake=Serialized), 201



@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.get_json()
    print("recived data:", data)

    if not all(k in data for k in ["flavor", "size", "rating"]):
        return jsonify({"error": "Missing required fields"}), 400

    cupcake.flavor = data.get("flavor", cupcake.flavor)
    cupcake.size = data.get("size", cupcake.size)
    cupcake.rating = data.get("rating", cupcake.rating)
    cupcake.image = data.get("image", cupcake.image)

    serialized = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error during database commit:", e)
        return jsonify({"error": "database error"}), 500

    return jsonify(cupcake=serialized), 200



@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake."""
    

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Daftar paket wisata dan harga
packages = {
    "Lake Toba Adventure": {
        "price": 750000,
        "duration": "2 Days 1 Night",
        "description": "Enjoy the beautiful scenery of Lake Toba and Samosir Island."
    },
    "Berastagi Highland Tour": {
        "price": 500000,
        "duration": "1 Day",
        "description": "Explore the beautiful mountains, gardens, and fresh air of Berastagi."
    },
    "Medan Heritage Tour": {
        "price": 350000,
        "duration": "1 Day",
        "description": "Discover the history, culture, and traditional architecture of Medan."
    },
    "Nias Cultural Experience": {
        "price": 900000,
        "duration": "3 Days 2 Nights",
        "description": "Experience the unique traditions and cultural beauty of Nias."
    }
}

@app.route("/")
def home():
    return render_template("index.html", packages=packages)

@app.route("/booking", methods=["POST"])
def booking():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    destination = request.form.get("destination", "")
    travel_date = request.form.get("travel_date", "")
    participants_text = request.form.get("participants", "")

    # Validasi formulir
    if not all([name, email, phone, destination,
                travel_date, participants_text]):
        return render_template(
            "index.html",
            packages=packages,
            error="Please complete all booking fields."
        )

    if destination not in packages:
        return render_template(
            "index.html",
            packages=packages,
            error="Please select a valid tour package."
        )

    try:
        participants = int(participants_text)
        selected_date = datetime.strptime(
            travel_date, "%Y-%m-%d"
        ).date()

        if participants < 1 or participants > 20:
            raise ValueError

        if selected_date < datetime.today().date():
            raise ValueError

    except ValueError:
        return render_template(
            "index.html",
            packages=packages,
            error="Please check your travel date and participant number."
        )

    # Menghitung total harga
    package_price = packages[destination]["price"]
    total_price = package_price * participants

    # Menampilkan halaman konfirmasi
    return render_template(
        "booking_success.html",
        name=name,
        email=email,
        phone=phone,
        destination=destination,
        travel_date=travel_date,
        participants=participants,
        package_price=package_price,
        total_price=total_price
    )

if __name__ == "__main__":
    app.run(debug=True)
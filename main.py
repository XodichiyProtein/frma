from flask import Flask, render_template, request, jsonify, redirect
import stripe
import os
from dotenv import load_dotenv

# Загружаем ключи из .env
load_dotenv()

app = Flask(__name__)

# Ключи Stripe (замените на свои!)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")


@app.route("/")
def home():
    return render_template("index.html", stripe_public_key=STRIPE_PUBLIC_KEY)


@app.route("/create-payment", methods=["POST"])
def create_payment():
    data = request.json
    nickname = data.get("nickname")
    amount = int(float(data.get("amount"))) * 100  # Stripe принимает сумму в центах

    try:
        # Создаем платежную сессию в Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Донат в Minecraft",
                        "description": f"Ник: {nickname}"  # Добавляем ник игрока
                    },
                    "unit_amount": amount,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://ваш-сайт.ру/success",
            cancel_url="https://ваш-сайт.ру/cancel",
        )
        return jsonify({"id": session.id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
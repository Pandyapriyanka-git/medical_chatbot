from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import gradio as gr
from utils import find_most_relevant_answer



from model import db, User, MedicalProduct, Cart
from db import init_db, get_all_diseases, save_chat, get_chat_history, delete_chat
from speech import speak, recognize_voice
from utils import find_most_relevant_answer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'simple'

db.init_app(app)
cache = Cache(app)

# Initialize DB inside app context
with app.app_context():
    db.create_all()
    init_db()

# Chatbot Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    diseases = get_all_diseases()
    result = find_most_relevant_answer(question, diseases)

    if result:
        answer = (
            f"Disease: {result['name']}\n"
            f"Description: {result['description']}\n"
            f"Symptoms: {result['symptoms']}\n"
            f"Treatments: {result['treatments']}"
        )
    else:
        answer = "Sorry, I couldn't find any matching information."

    save_chat(question, answer)
    speak(answer)
    return jsonify({'question': question, 'answer': answer})

@app.route('/voice_input')
def voice_input():
    return recognize_voice()

@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        delete_chat(request.form.get('question'))
    chats = get_chat_history()
    return render_template("admin.html", history=chats)

@app.route('/admin')
def admin():
    chats = get_chat_history()
    return render_template("admin.html", history=chats)

# Cart Routes
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    user_id = 1  # Replace with dynamic user ID if you have authentication
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', default=1, type=int)

    if not product_id:
        return redirect(url_for('index'))

    existing = Cart.query.filter_by(user_id=user_id, medical_product_id=product_id).first()
    if existing:
        existing.quantity += quantity
    else:
        db.session.add(Cart(user_id=user_id, medical_product_id=product_id, quantity=quantity))
    db.session.commit()

    return redirect(url_for('view_cart'))

@app.route('/view_cart')
def view_cart():
    user_id = 1  # Replace with session or dynamic user ID
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    item = Cart.query.get(cart_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('view_cart'))

@app.route('/update_quantity/<int:cart_id>', methods=['POST'])
def update_quantity(cart_id):
    new_qty = request.form.get('quantity', type=int)
    item = Cart.query.get(cart_id)
    if item and new_qty > 0:
        item.quantity = new_qty
        db.session.commit()
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)

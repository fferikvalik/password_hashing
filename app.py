from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Для сообщений с flash

# Переменная для хранения хэша пароля
stored_password_hash = None

# Функция для создания хэша пароля
def create_hash(password):
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()

# Функция для проверки пароля
def verify_password(stored_hash, password):
    return stored_hash == create_hash(password)

@app.route('/', methods=['GET', 'POST'])
def home():
    global stored_password_hash
    
    if request.method == 'POST':
        password = request.form['password']
        
        # Хэшируем и сохраняем пароль
        stored_password_hash = create_hash(password)
        
        flash("Пароль успешно сохранён!", "success")
        return redirect(url_for('verify'))
    
    return render_template('index.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        attempt = request.form['password']
        
        if stored_password_hash is None:
            flash("Пароль ещё не установлен!", "danger")
        elif verify_password(stored_password_hash, attempt):
            flash("Пароль введён правильно!", "success")
        else:
            flash("Неверный пароль!", "danger")
    
    return render_template('verify.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        nik    = request.form.get('nik', '').strip()
        nama   = request.form.get('nama', '').strip()
        email  = request.form.get('email', '').strip()
        telepon= request.form.get('telepon', '').strip()
        alamat = request.form.get('alamat', '').strip()
        pw     = request.form.get('password', '')
        pw2    = request.form.get('confirm_password', '')
        
        if pw != pw2:
            flash('Password tidak cocok.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(nik=nik).first():
            flash('NIK sudah terdaftar.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar.', 'danger')
            return render_template('register.html')
        
        user = User(nik=nik, nama=nama, email=email,
                    telepon=telepon, alamat=alamat)
        user.set_password(pw)
        db.session.add(user)
        db.session.commit()
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        pw    = request.form.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(pw):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Selamat datang, {user.nama}!', 'success')
            return redirect(next_page or url_for('main.index'))
        
        flash('Email atau password salah.', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('main.index'))
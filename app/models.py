from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id         = db.Column(db.Integer, primary_key=True)
    nik        = db.Column(db.String(16), unique=True, nullable=False)
    nama       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    telepon    = db.Column(db.String(15))
    alamat     = db.Column(db.Text)
    password   = db.Column(db.String(256), nullable=False)
    role       = db.Column(db.String(10), default='warga')  # warga / admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    surats    = db.relationship('Surat', backref='pemohon', lazy=True)
    pengaduans = db.relationship('Pengaduan', backref='pelapor', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Surat(db.Model):
    __tablename__ = 'surats'
    
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    jenis_surat = db.Column(db.String(50), nullable=False)
    keperluan   = db.Column(db.Text, nullable=False)
    status      = db.Column(db.String(20), default='pending')
    # pending / diproses / selesai / ditolak
    keterangan  = db.Column(db.Text)
    file_url    = db.Column(db.String(500))   # S3 URL lampiran
    hasil_url   = db.Column(db.String(500))   # S3 URL surat hasil
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow)


class Pengaduan(db.Model):
    __tablename__ = 'pengaduans'
    
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    judul       = db.Column(db.String(200), nullable=False)
    isi         = db.Column(db.Text, nullable=False)
    kategori    = db.Column(db.String(50))
    status      = db.Column(db.String(20), default='masuk')
    # masuk / ditindak / selesai
    foto_url    = db.Column(db.String(500))   # S3 URL foto bukti
    tanggapan   = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow)
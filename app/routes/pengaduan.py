import boto3, uuid
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, current_app)
from flask_login import login_required, current_user
from app.models import db, Pengaduan

pengaduan_bp = Blueprint('pengaduan', __name__)

KATEGORI = ['Infrastruktur', 'Kebersihan', 'Keamanan',
            'Pelayanan', 'Sosial', 'Lainnya']

def upload_to_s3(file, folder='pengaduan'):
    s3 = boto3.client(
        's3',
        aws_access_key_id     = current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key = current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name           = current_app.config['AWS_REGION'],
    )
    bucket   = current_app.config['S3_BUCKET']
    ext      = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{folder}/{uuid.uuid4().hex}.{ext}"
    s3.upload_fileobj(file, bucket, filename,
                      ExtraArgs={'ContentType': file.content_type})
    region = current_app.config['AWS_REGION']
    return f"https://{bucket}.s3.{region}.amazonaws.com/{filename}"


@pengaduan_bp.route('/')
@login_required
def list_pengaduan():
    if current_user.role == 'admin':
        return redirect(url_for('admin.kelola_pengaduan'))
    data = Pengaduan.query.filter_by(user_id=current_user.id)\
                          .order_by(Pengaduan.created_at.desc()).all()
    return render_template('pengaduan/list.html', pengaduans=data)


@pengaduan_bp.route('/buat', methods=['GET', 'POST'])
@login_required
def buat():
    if request.method == 'POST':
        judul    = request.form.get('judul', '').strip()
        isi      = request.form.get('isi', '').strip()
        kategori = request.form.get('kategori')
        foto     = request.files.get('foto')
        
        if not judul or not isi:
            flash('Judul dan isi pengaduan wajib diisi.', 'danger')
            return render_template('pengaduan/buat.html', kategori_list=KATEGORI)
        
        foto_url = None
        if foto and foto.filename:
            foto_url = upload_to_s3(foto)
        
        p = Pengaduan(user_id=current_user.id, judul=judul,
                      isi=isi, kategori=kategori, foto_url=foto_url)
        db.session.add(p)
        db.session.commit()
        
        flash('Pengaduan berhasil dikirim!', 'success')
        return redirect(url_for('pengaduan.list_pengaduan'))
    
    return render_template('pengaduan/buat.html', kategori_list=KATEGORI)
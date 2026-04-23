import boto3, uuid, os
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, current_app)
from flask_login import login_required, current_user
from app.models import db, Surat

surat_bp = Blueprint('surat', __name__)

JENIS_SURAT = [
    'Surat Domisili',
    'Surat Keterangan Usaha',
    'Surat Keterangan Tidak Mampu',
    'Surat Pengantar KTP',
    'Surat Keterangan Kelahiran',
    'Surat Keterangan Kematian',
]

def upload_to_s3(file, folder='lampiran'):
    """Upload file ke S3, return public URL."""
    s3 = boto3.client(
        's3',
        region_name = os.environ.get('AWS_REGION', 'ap-southeast-1'),
    )
    bucket = current_app.config['S3_BUCKET']
    ext      = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{folder}/{uuid.uuid4().hex}.{ext}"
    
    s3.upload_fileobj(
        file,
        bucket,
        filename,
        ExtraArgs={'ContentType': file.content_type}
    )
    region = current_app.config['AWS_REGION']
    return f"https://{bucket}.s3.{region}.amazonaws.com/{filename}"


def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower()
            in current_app.config['ALLOWED_EXTENSIONS'])


@surat_bp.route('/')
@login_required
def list_surat():
    if current_user.role == 'admin':
        return redirect(url_for('admin.kelola_surat'))
    surats = Surat.query.filter_by(user_id=current_user.id)\
                        .order_by(Surat.created_at.desc()).all()
    return render_template('surat/list.html', surats=surats)


@surat_bp.route('/ajukan', methods=['GET', 'POST'])
@login_required
def ajukan():
    if request.method == 'POST':
        jenis    = request.form.get('jenis_surat')
        keperluan= request.form.get('keperluan', '').strip()
        file     = request.files.get('lampiran')
        
        if not jenis or not keperluan:
            flash('Jenis surat dan keperluan wajib diisi.', 'danger')
            return render_template('surat/ajukan.html', jenis_list=JENIS_SURAT)
        
        file_url = None
        if file and file.filename and allowed_file(file.filename):
            file_url = upload_to_s3(file, folder='lampiran')
        
        surat = Surat(user_id=current_user.id,
                      jenis_surat=jenis,
                      keperluan=keperluan,
                      file_url=file_url)
        db.session.add(surat)
        db.session.commit()
        
        flash('Pengajuan surat berhasil dikirim!', 'success')
        return redirect(url_for('surat.list_surat'))
    
    return render_template('surat/ajukan.html', jenis_list=JENIS_SURAT)


@surat_bp.route('/<int:surat_id>')
@login_required
def detail(surat_id):
    surat = Surat.query.get_or_404(surat_id)
    if surat.user_id != current_user.id and current_user.role != 'admin':
        flash('Akses ditolak.', 'danger')
        return redirect(url_for('surat.list_surat'))
    return render_template('surat/detail.html', surat=surat)
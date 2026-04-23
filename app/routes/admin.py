from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request)
from flask_login import login_required, current_user
from functools import wraps
from app.models import db, Surat, Pengaduan, User

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Akses admin diperlukan.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_surat     = Surat.query.count()
    pending_surat   = Surat.query.filter_by(status='pending').count()
    total_pengaduan = Pengaduan.query.count()
    total_warga     = User.query.filter_by(role='warga').count()
    return render_template('admin/dashboard.html',
                           total_surat=total_surat,
                           pending_surat=pending_surat,
                           total_pengaduan=total_pengaduan,
                           total_warga=total_warga)


@admin_bp.route('/surat')
@login_required
@admin_required
def kelola_surat():
    status = request.args.get('status', '')
    q = Surat.query
    if status:
        q = q.filter_by(status=status)
    surats = q.order_by(Surat.created_at.desc()).all()
    return render_template('admin/surat.html', surats=surats, status=status)


@admin_bp.route('/surat/<int:surat_id>/update', methods=['POST'])
@login_required
@admin_required
def update_surat(surat_id):
    surat = Surat.query.get_or_404(surat_id)
    surat.status     = request.form.get('status', surat.status)
    surat.keterangan = request.form.get('keterangan', '')
    db.session.commit()
    flash('Status surat diperbarui.', 'success')
    return redirect(url_for('admin.kelola_surat'))


@admin_bp.route('/pengaduan')
@login_required
@admin_required
def kelola_pengaduan():
    data = Pengaduan.query.order_by(Pengaduan.created_at.desc()).all()
    return render_template('admin/pengaduan.html', pengaduans=data)


@admin_bp.route('/pengaduan/<int:p_id>/update', methods=['POST'])
@login_required
@admin_required
def update_pengaduan(p_id):
    p = Pengaduan.query.get_or_404(p_id)
    p.status     = request.form.get('status', p.status)
    p.tanggapan  = request.form.get('tanggapan', '')
    db.session.commit()
    flash('Status pengaduan diperbarui.', 'success')
    return redirect(url_for('admin.kelola_pengaduan'))
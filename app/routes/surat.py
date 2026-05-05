{% extends 'base.html' %}
{% block title %}Dashboard - SiPelDes{% endblock %}
{% block content %}

<div class="row g-4">
  <!-- Welcome Banner -->
  <div class="col-12">
    <div class="p-4 rounded-3" style="background: linear-gradient(135deg, #1a5276, #2e86c1);">
      <h4 class="text-white fw-bold mb-1">
        👋 Selamat datang, {{ current_user.nama }}!
      </h4>
      <p class="text-white opacity-75 mb-0">
        Selamat menggunakan SiPelDes — Sistem Pelayanan Desa Digital. 
        Layanan administrasi desa kini lebih mudah dan cepat secara online.
      </p>
    </div>
  </div>

  <!-- Info Aplikasi -->
  <div class="col-12">
    <div class="card border-0 shadow-sm">
      <div class="card-body p-4">
        <h5 class="fw-bold mb-3"><i class="bi bi-info-circle text-primary"></i> Tentang SiPelDes</h5>
        <p class="text-muted mb-0">
          <strong>SiPelDes (Sistem Pelayanan Desa)</strong> adalah platform digital yang dirancang 
          untuk memudahkan warga desa dalam mengakses layanan administrasi secara online. 
          Dengan SiPelDes, Anda dapat mengajukan surat keterangan, memantau status pengajuan, 
          dan menyampaikan pengaduan kepada pemerintah desa kapan saja dan di mana saja 
          tanpa perlu datang langsung ke kantor desa.
        </p>
      </div>
    </div>
  </div>

  <!-- Layanan -->
  <div class="col-12">
    <h5 class="fw-bold mb-3">Layanan Tersedia</h5>
  </div>

  <div class="col-md-4">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body p-4 text-center">
        <i class="bi bi-file-earmark-text fs-1 text-primary mb-3 d-block"></i>
        <h6 class="fw-bold">Pengajuan Surat</h6>
        <p class="text-muted small mb-3">
          Ajukan surat keterangan domisili, usaha, tidak mampu, dan lainnya secara online.
        </p>
        <a href="{{ url_for('surat.ajukan') }}" class="btn btn-primary btn-sm">
          <i class="bi bi-plus-circle"></i> Ajukan Sekarang
        </a>
      </div>
    </div>
  </div>

  <div class="col-md-4">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body p-4 text-center">
        <i class="bi bi-clock-history fs-1 text-success mb-3 d-block"></i>
        <h6 class="fw-bold">Status Pengajuan</h6>
        <p class="text-muted small mb-3">
          Pantau perkembangan pengajuan surat Anda secara real-time.
        </p>
        <a href="{{ url_for('surat.list_surat') }}" class="btn btn-success btn-sm">
          <i class="bi bi-search"></i> Lihat Status
        </a>
      </div>
    </div>
  </div>

  <div class="col-md-4">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body p-4 text-center">
        <i class="bi bi-megaphone fs-1 text-warning mb-3 d-block"></i>
        <h6 class="fw-bold">Pengaduan Warga</h6>
        <p class="text-muted small mb-3">
          Sampaikan aspirasi dan pengaduan kepada pemerintah desa disertai foto bukti.
        </p>
        <a href="{{ url_for('pengaduan.buat') }}" class="btn btn-warning btn-sm">
          <i class="bi bi-megaphone"></i> Buat Pengaduan
        </a>
      </div>
    </div>
  </div>

  <!-- Info Akun -->
  <div class="col-12">
    <div class="card border-0 shadow-sm">
      <div class="card-body p-4">
        <h5 class="fw-bold mb-3"><i class="bi bi-person-circle text-secondary"></i> Informasi Akun</h5>
        <div class="row">
          <div class="col-md-6">
            <table class="table table-borderless mb-0">
              <tr><td class="text-muted" width="40%">Nama</td><td><strong>{{ current_user.nama }}</strong></td></tr>
              <tr><td class="text-muted">NIK</td><td><strong>{{ current_user.nik }}</strong></td></tr>
              <tr><td class="text-muted">Email</td><td><strong>{{ current_user.email }}</strong></td></tr>
            </table>
          </div>
          <div class="col-md-6">
            <table class="table table-borderless mb-0">
              <tr><td class="text-muted" width="40%">Telepon</td><td><strong>{{ current_user.telepon or '-' }}</strong></td></tr>
              <tr><td class="text-muted">Alamat</td><td><strong>{{ current_user.alamat or '-' }}</strong></td></tr>
              <tr><td class="text-muted">Role</td><td><span class="badge bg-primary">{{ current_user.role }}</span></td></tr>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

</div>
{% endblock %}

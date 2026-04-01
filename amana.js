const actsData = [
  { type: 'positive', student: 'Yasmine Trabelsi', class: '4A', category: 'Talent académique', desc: 'Excellente présentation orale sur l'environnement. Initiative remarquable.', date: 'Aujourd\'hui 09h30', badge: 'Talent' },
  { type: 'negative', student: 'Karim Mansour', class: '4B', category: 'Agressivité', desc: 'Comportement agressif envers un camarade pendant la récréation.', date: 'Hier 14h15', badge: 'Alerte' },
  { type: 'positive', student: 'Sonia Gharbi', class: '4C', category: 'Solidarité', desc: 'A aidé spontanément plusieurs élèves en difficulté en mathématiques.', date: 'Hier 11h00', badge: 'Solidarité' },
  { type: 'neutral', student: 'Mohamed Ayari', class: '4B', category: 'Retards répétés', desc: 'Retard répété (5e fois ce mois). Comportement inhabituel et renfermé.', date: 'Il y a 2 jours', badge: 'À surveiller' },
  { type: 'positive', student: 'Ines Bouaziz', class: '4A', category: 'Créativité', desc: 'Projet artistique remarquable présenté au concours régional.', date: 'Il y a 3 jours', badge: 'Créativité' },
  { type: 'negative', student: 'Rami Chabbi', class: '4C', category: 'Désengagement scolaire', desc: 'Baisse soudaine des résultats, manque de participation en classe.', date: 'Il y a 4 jours', badge: 'Alerte' },
  { type: 'positive', student: 'Dorra Khalil', class: '4A', category: 'Leadership', desc: 'A pris l\'initiative d\'organiser une collecte de fournitures pour des élèves dans le besoin.', date: 'Il y a 5 jours', badge: 'Leadership' },
];

const studentsData = [
  { name: 'Yasmine Trabelsi', class: '4ème A', initials: 'YT', color: '#e6faf8', textColor: '#0F6E56', score: 92, risk: 'low' },
  { name: 'Karim Mansour', class: '4ème B', initials: 'KM', color: '#fff1f2', textColor: '#e11d48', score: 24, risk: 'high' },
  { name: 'Sonia Gharbi', class: '4ème C', initials: 'SG', color: '#e6faf8', textColor: '#0F6E56', score: 88, risk: 'low' },
  { name: 'Mohamed Ayari', class: '4ème B', initials: 'MA', color: '#fffbeb', textColor: '#d97706', score: 45, risk: 'medium' },
  { name: 'Ines Bouaziz', class: '4ème A', initials: 'IB', color: '#e6faf8', textColor: '#0F6E56', score: 80, risk: 'low' },
  { name: 'Rami Chabbi', class: '4ème C', initials: 'RC', color: '#fffbeb', textColor: '#d97706', score: 55, risk: 'medium' },
  { name: 'Dorra Khalil', class: '4ème A', initials: 'DK', color: '#e6faf8', textColor: '#0F6E56', score: 95, risk: 'low' },
  { name: 'Ali Bouchnak', class: '4ème B', initials: 'AB', color: '#e6faf8', textColor: '#0F6E56', score: 70, risk: 'low' },
];

const pageLabels = { dashboard:'Tableau de bord', declare:'Déclarer un acte', history:'Historique des actes', students:'Mes élèves', alerts:'Alertes', parents:'Contacter parents', psychiatrists:'Psychiatres' };

function showPage(id, el) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById('page-' + id).classList.add('active');
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  if (el) el.classList.add('active');
  document.getElementById('topbar-title').textContent = pageLabels[id] || '';
  if (id === 'history') renderHistory();
  if (id === 'students') renderStudents();
  if (window.innerWidth <= 768) document.getElementById('sidebar').classList.remove('open');
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

function renderHistory(filter = {}) {
  const list = document.getElementById('acts-list');
  let data = actsData;
  if (filter.type) data = data.filter(a => a.type === filter.type);
  if (filter.class) data = data.filter(a => a.class === filter.class.replace('ème ',''));
  list.innerHTML = data.map(a => `
    <div class="act-item">
      <div class="act-dot ${a.type}"></div>
      <div style="flex:1">
        <div class="act-student">${a.student}</div>
        <div class="act-desc">${a.desc}</div>
        <div class="act-meta"><i class="bi bi-clock me-1"></i>${a.date} · ${a.class} · ${a.category}</div>
      </div>
      <span class="badge-act ${a.type}">${a.badge}</span>
    </div>
  `).join('');
}

document.getElementById('filterType').addEventListener('change', function() {
  renderHistory({ type: this.value, class: document.getElementById('filterClass').value });
});
document.getElementById('filterClass').addEventListener('change', function() {
  renderHistory({ type: document.getElementById('filterType').value, class: this.value });
});

function renderStudents(filter = '') {
  const grid = document.getElementById('students-grid');
  const data = filter ? studentsData.filter(s => s.name.toLowerCase().includes(filter.toLowerCase())) : studentsData;
  const riskLabel = { high: 'Risque élevé', medium: 'Surveillance', low: 'Bon suivi' };
  const scoreColor = { high: '#e11d48', medium: '#f59e0b', low: '#059669' };
  grid.innerHTML = data.map(s => `
    <div class="col-6 col-md-4 col-lg-3">
      <div class="student-card">
        <div class="student-avatar" style="background:${s.color};color:${s.textColor}">${s.initials}</div>
        <div class="student-name">${s.name}</div>
        <div class="student-class">${s.class}</div>
        <div class="student-score mt-3">
          <span style="font-size:12px;color:var(--text-muted);">Score</span>
          <div class="score-bar"><div class="score-fill" style="width:${s.score}%;background:${scoreColor[s.risk]}"></div></div>
          <span style="color:${scoreColor[s.risk]}">${s.score}</span>
        </div>
        <div class="d-flex align-items-center justify-content-between mt-2">
          <span class="risk-badge ${s.risk}">${riskLabel[s.risk]}</span>
          <button class="btn-contact secondary" style="font-size:11px;padding:4px 10px;" onclick="toast('📋 Profil de ${s.name} — À implémenter')">Profil</button>
        </div>
      </div>
    </div>
  `).join('');
}

let selectedType = 'positive';
function selectType(type, el) {
  document.querySelectorAll('.type-btn').forEach(b => b.classList.remove('selected'));
  el.classList.add('selected');
  selectedType = type;
}

function submitAct() {
  const student = document.getElementById('studentSelect').value;
  const desc = document.getElementById('descInput').value;
  if (!student || !desc) { toast('⚠️ Veuillez remplir tous les champs obligatoires.'); return; }
  actsData.unshift({ type: selectedType, student: student.split(' (')[0], class: student.match(/\(([^)]+)\)/)?.[1]?.replace('ème ','') || '4A', category: document.getElementById('categorySelect').value || 'Autre', desc, date: 'À l\'instant', badge: selectedType === 'positive' ? 'Nouveau' : selectedType === 'negative' ? 'Alerte' : 'À surveiller' });
  toast('✅ Acte enregistré avec succès !');
  clearForm();
}

function clearForm() {
  document.getElementById('studentSelect').value = '';
  document.getElementById('categorySelect').value = '';
  document.getElementById('descInput').value = '';
  document.getElementById('dateInput').value = '';
  document.querySelectorAll('#recommendations input').forEach(c => c.checked = false);
}

function openContactModal(student, parent, phone) {
  document.getElementById('modal-parent-name').textContent = 'Contacter ' + parent;
  document.getElementById('modal-student-info').textContent = 'Concernant : ' + student + ' · ' + phone;
  document.getElementById('contactModal').classList.add('show');
}
function closeModal() { document.getElementById('contactModal').classList.remove('show'); }
function sendMessage() { closeModal(); toast('✉️ Message envoyé aux parents avec succès !'); }

function openMailModal(parent, student) {
  document.getElementById('mail-parent-name').textContent = 'Message à ' + parent;
  document.getElementById('mail-student-info').textContent = 'Concernant : ' + student;
  document.getElementById('mailModal').classList.add('show');
}
function closeMailModal() { document.getElementById('mailModal').classList.remove('show'); }
function sendMail() { closeMailModal(); toast('✉️ Message envoyé avec succès !'); }

document.getElementById('contactModal').addEventListener('click', function(e) { if(e.target===this) closeModal(); });
document.getElementById('mailModal').addEventListener('click', function(e) { if(e.target===this) closeMailModal(); });

function toast(msg) {
  const c = document.getElementById('toastContainer');
  const t = document.createElement('div');
  t.className = 'toast-msg';
  t.innerHTML = msg;
  c.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

function globalSearch(val) {
  if (val.length > 1) { renderStudents(val); showPage('students', null); }
}

document.addEventListener('DOMContentLoaded', () => {
  const now = new Date();
  const pad = n => String(n).padStart(2,'0');
  document.getElementById('dateInput').value = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`;
  renderHistory();
  renderStudents();
});
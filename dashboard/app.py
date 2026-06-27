import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from data.database import get_all_leads, get_stats

app = Flask(__name__)
CORS(app)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>AI Automation Hub</title>
  <meta charset="utf-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: system-ui, sans-serif; 
      background: #0f0f0f; 
      color: #e5e5e5; 
      padding: 2rem;
    }
    .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 2rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid #2a2a2a;
    }
    .header h1 { 
      font-size: 1.4rem; 
      font-weight: 500;
      color: #fff;
    }
    .live-dot {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: #4ade80;
    }
    .dot {
      width: 8px; height: 8px;
      background: #4ade80;
      border-radius: 50%;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.3; }
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px;
      margin-bottom: 2rem;
    }
    .stat-card {
      background: #1a1a1a;
      border: 1px solid #2a2a2a;
      border-radius: 10px;
      padding: 1.2rem;
    }
    .stat-label { 
      font-size: 11px; 
      color: #666; 
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }
    .stat-value { 
      font-size: 32px; 
      font-weight: 600;
      color: #fff;
    }
    .stat-card.total .stat-value { color: #a78bfa; }
    .stat-card.hot .stat-value { color: #4ade80; }
    .stat-card.support .stat-value { color: #60a5fa; }
    .stat-card.spam .stat-value { color: #f87171; }
    .section-title {
      font-size: 13px;
      color: #666;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 12px;
    }
    .table-wrap {
      background: #1a1a1a;
      border: 1px solid #2a2a2a;
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 2rem;
    }
    table { width: 100%; border-collapse: collapse; }
    th { 
      text-align: left; 
      padding: 12px 16px; 
      font-size: 11px; 
      color: #555;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      border-bottom: 1px solid #2a2a2a;
    }
    td { 
      padding: 12px 16px; 
      font-size: 13px; 
      border-bottom: 1px solid #1f1f1f;
      vertical-align: top;
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: #222; }
    .badge { 
      padding: 3px 10px; 
      border-radius: 20px; 
      font-size: 11px; 
      font-weight: 500;
      display: inline-block;
    }
    .hot_lead { background: #052e16; color: #4ade80; border: 1px solid #166534; }
    .cold_lead { background: #0c1a2e; color: #60a5fa; border: 1px solid #1e3a5f; }
    .spam { background: #2d0a0a; color: #f87171; border: 1px solid #7f1d1d; }
    .support { background: #0c1a2e; color: #93c5fd; border: 1px solid #1e3a5f; }
    .partnership { background: #1a0a2e; color: #c084fc; border: 1px solid #4a1d7f; }
    .priority-high { color: #f87171; font-size: 12px; }
    .priority-medium { color: #fbbf24; font-size: 12px; }
    .priority-low { color: #6b7280; font-size: 12px; }
    .summary-text { 
      color: #888; 
      font-size: 12px; 
      margin-top: 4px;
      max-width: 300px;
    }
    .reply-box {
      background: #111;
      border: 1px solid #2a2a2a;
      border-radius: 8px;
      padding: 1.2rem;
      margin-bottom: 12px;
    }
    .reply-from { 
      font-size: 12px; 
      color: #555; 
      margin-bottom: 8px;
    }
    .reply-text { 
      font-size: 13px; 
      color: #ccc;
      line-height: 1.6;
    }
    .empty { 
      text-align: center; 
      padding: 3rem;
      color: #444;
      font-size: 14px;
    }
    .refresh-btn {
      background: #1a1a1a;
      border: 1px solid #2a2a2a;
      color: #888;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
    }
    .refresh-btn:hover { background: #222; color: #ccc; }
  </style>
</head>
<body>

<div class="header">
  <h1>AI Automation Hub</h1>
  <div style="display:flex;align-items:center;gap:12px">
    <div class="live-dot">
      <div class="dot"></div>
      Live Dashboard
    </div>
    <button class="refresh-btn" onclick="loadData()">Refresh</button>
  </div>
</div>

<div class="stats" id="stats">
  <div class="stat-card total">
    <div class="stat-label">Total Processed</div>
    <div class="stat-value" id="stat-total">—</div>
  </div>
  <div class="stat-card hot">
    <div class="stat-label">Hot Leads</div>
    <div class="stat-value" id="stat-hot">—</div>
  </div>
  <div class="stat-card support">
    <div class="stat-label">Support</div>
    <div class="stat-value" id="stat-support">—</div>
  </div>
  <div class="stat-card spam">
    <div class="stat-label">Spam Blocked</div>
    <div class="stat-value" id="stat-spam">—</div>
  </div>
</div>

<div class="section-title">All Processed Emails</div>
<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>Sender</th>
        <th>Subject</th>
        <th>Category</th>
        <th>Priority</th>
        <th>Summary</th>
        <th>Time</th>
      </tr>
    </thead>
    <tbody id="leads-table">
      <tr><td colspan="6" class="empty">Loading...</td></tr>
    </tbody>
  </table>
</div>

<div class="section-title">AI Generated Replies</div>
<div id="replies-section">
  <div class="empty">Loading...</div>
</div>

<script>
function loadData() {
  fetch('/api/stats')
    .then(r => r.json())
    .then(data => {
      document.getElementById('stat-total').textContent = data.total || 0;
      document.getElementById('stat-hot').textContent = data.hot_lead || 0;
      document.getElementById('stat-support').textContent = data.support || 0;
      document.getElementById('stat-spam').textContent = data.spam || 0;
    });

  fetch('/api/leads')
    .then(r => r.json())
    .then(leads => {
      const tbody = document.getElementById('leads-table');
      const repliesDiv = document.getElementById('replies-section');

      if (leads.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty">No emails processed yet.</td></tr>';
        repliesDiv.innerHTML = '<div class="empty">No replies generated yet.</div>';
        return;
      }

      tbody.innerHTML = leads.map(lead => `
        <tr>
          <td>${lead.sender}</td>
          <td style="max-width:200px">${lead.subject || '—'}</td>
          <td><span class="badge ${lead.category}">${(lead.category || '').replace('_', ' ')}</span></td>
          <td><span class="priority-${lead.priority}">${lead.priority || '—'}</span></td>
          <td><div class="summary-text">${lead.summary || '—'}</div></td>
          <td style="color:#555;font-size:12px">${(lead.processed_at || '').slice(0, 16)}</td>
        </tr>
      `).join('');

      repliesDiv.innerHTML = leads
        .filter(l => l.suggested_reply)
        .map(lead => `
          <div class="reply-box">
            <div class="reply-from">
              To: ${lead.sender} &nbsp;·&nbsp; 
              <span class="badge ${lead.category}">${(lead.category || '').replace('_', ' ')}</span>
            </div>
            <div class="reply-text">${lead.suggested_reply}</div>
          </div>
        `).join('');
    });
}

loadData();
setInterval(loadData, 10000);
</script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML)

@app.route('/api/leads')
def api_leads():
    return jsonify(get_all_leads())

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

if __name__ == '__main__':
    print("Dashboard running at http://localhost:5000")
    app.run(debug=True, port=5000)
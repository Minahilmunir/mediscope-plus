import React, { useState, useEffect, useRef, useCallback } from "react";
import "./App.css";

const API = "http://127.0.0.1:5000";

// -- Neural Canvas Background --
function NeuralCanvas() {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    let animId;
    let W, H;
    const NODES = 50;
    const nodes = [];
    function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
    function init() {
      nodes.length = 0;
      for (let i = 0; i < NODES; i++)
        nodes.push({ x: Math.random()*W, y: Math.random()*H, vx:(Math.random()-0.5)*0.3, vy:(Math.random()-0.5)*0.3, r:Math.random()*1.5+0.5, pulse:Math.random()*Math.PI*2 });
    }
    function draw() {
      ctx.clearRect(0,0,W,H);
      nodes.forEach(n => {
        n.x+=n.vx; n.y+=n.vy; n.pulse+=0.015;
        if(n.x<0||n.x>W) n.vx*=-1;
        if(n.y<0||n.y>H) n.vy*=-1;
        const a = 0.3+0.2*Math.sin(n.pulse);
        ctx.beginPath(); ctx.arc(n.x,n.y,n.r,0,Math.PI*2);
        ctx.fillStyle=`rgba(52,211,153,${a})`; ctx.shadowBlur=6; ctx.shadowColor="rgba(16,185,129,0.5)"; ctx.fill(); ctx.shadowBlur=0;
      });
      for(let i=0;i<nodes.length;i++) for(let j=i+1;j<nodes.length;j++) {
        const dx=nodes[i].x-nodes[j].x, dy=nodes[i].y-nodes[j].y, d=Math.sqrt(dx*dx+dy*dy);
        if(d<160) { ctx.beginPath(); ctx.moveTo(nodes[i].x,nodes[i].y); ctx.lineTo(nodes[j].x,nodes[j].y); ctx.strokeStyle=`rgba(16,185,129,${(1-d/160)*0.08})`; ctx.lineWidth=1; ctx.stroke(); }
      }
      animId = requestAnimationFrame(draw);
    }
    resize(); init(); draw();
    window.addEventListener("resize",()=>{resize();init();});
    return ()=>{ cancelAnimationFrame(animId); };
  },[]);
  return <canvas ref={canvasRef} className="neural-canvas"/>;
}

// -- Urgency Config --
const URGENCY = {
  critical: { label:"CRITICAL",  color:"#ef4444", bg:"rgba(239,68,68,0.1)",   border:"rgba(239,68,68,0.3)",   icon:"🚨" },
  high:     { label:"HIGH",      color:"#f97316", bg:"rgba(249,115,22,0.1)",  border:"rgba(249,115,22,0.3)",  icon:"⚠️" },
  medium:   { label:"MEDIUM",    color:"#f59e0b", bg:"rgba(245,158,11,0.1)",  border:"rgba(245,158,11,0.3)",  icon:"📋" },
  low:      { label:"LOW",       color:"#10b981", bg:"rgba(16,185,129,0.1)",  border:"rgba(16,185,129,0.3)",  icon:"✅" },
};

const VITAL_STATUS = {
  critical: { color:"#ef4444", icon:"🔴" },
  high:     { color:"#f97316", icon:"🟠" },
  elevated: { color:"#f59e0b", icon:"🟡" },
  low:      { color:"#3b82f6", icon:"🔵" },
  normal:   { color:"#10b981", icon:"🟢" },
};

// -- Animated Score Ring --
function ScoreRing({ value, label, color, size=80 }) {
  const r = (size-10)/2, circ = 2*Math.PI*r;
  const dash = circ - (value/100)*circ;
  return (
    <div className="score-ring-wrap">
      <svg width={size} height={size}>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="5"/>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth="5"
          strokeDasharray={circ} strokeDashoffset={dash}
          strokeLinecap="round" transform={`rotate(-90 ${size/2} ${size/2})`}
          style={{transition:"stroke-dashoffset 1s ease"}}/>
      </svg>
      <div className="score-ring-inner">
        <span className="score-val" style={{color}}>{value}</span>
      </div>
      <span className="score-label">{label}</span>
    </div>
  );
}

// -- Typewriter --
function useTypewriter(text, speed=18) {
  const [out, setOut] = useState("");
  useEffect(()=>{
    setOut(""); if(!text) return;
    let i=0;
    const t=setInterval(()=>{ setOut(text.slice(0,++i)); if(i>=text.length) clearInterval(t); },speed);
    return ()=>clearInterval(t);
  },[text,speed]);
  return out;
}

// -- Tab Bar --
function TabBar({ tabs, active, onChange }) {
  return (
    <div className="tab-bar">
      {tabs.map(t=>(
        <button key={t.id} className={`tab-btn ${active===t.id?"active":""}`} onClick={()=>onChange(t.id)}>
          <span>{t.icon}</span> {t.label}
        </button>
      ))}
    </div>
  );
}

// -- Vitals Panel --
function VitalsPanel({ vitals, setVitals }) {
  const fields = [
    { key:"blood_pressure",    label:"Blood Pressure",   placeholder:"120/80",  unit:"mmHg", icon:"💉" },
    { key:"heart_rate",        label:"Heart Rate",        placeholder:"72",      unit:"bpm",  icon:"❤️" },
    { key:"temperature",       label:"Temperature",       placeholder:"37.0",    unit:"°C",   icon:"🌡️" },
    { key:"oxygen_saturation", label:"SpO₂",              placeholder:"98",      unit:"%",    icon:"💨" },
    { key:"blood_sugar",       label:"Blood Sugar",       placeholder:"90",      unit:"mg/dL",icon:"🩸" },
  ];
  return (
    <div className="vitals-grid">
      {fields.map(f=>(
        <div key={f.key} className="vital-field">
          <label className="vital-label"><span>{f.icon}</span> {f.label}</label>
          <div className="vital-input-wrap">
            <input type="text" className="vital-input" placeholder={f.placeholder}
              value={vitals[f.key]||""} onChange={e=>setVitals(v=>({...v,[f.key]:e.target.value}))}/>
            <span className="vital-unit">{f.unit}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

// -- Vitals Result --
function VitalsResult({ items }) {
  if(!items||!items.length) return null;
  return (
    <div className="vitals-result-grid">
      {items.map((item,i)=>{
        const cfg = VITAL_STATUS[item.status]||VITAL_STATUS.normal;
        return (
          <div key={i} className="vital-result-card" style={{"--vc":cfg.color}}>
            <div className="vrc-top">
              <span className="vrc-icon">{cfg.icon}</span>
              <span className="vrc-vital">{item.vital}</span>
              <span className="vrc-value" style={{color:cfg.color}}>{item.value}</span>
            </div>
            <p className="vrc-note">{item.note}</p>
          </div>
        );
      })}
    </div>
  );
}

// -- Diagnosis Result Panel --
function DiagnosisResult({ result, onReset }) {
  const [copied, setCopied] = useState(false);
  const urg = URGENCY[result.diagnosis.overall_urgency] || URGENCY.low;
  const symText = result.analysis.symptoms_recognized.join(", ") || "—";

  const copyReport = () => {
    const lines = [
      `MediScope+ Report — ${result.timestamp}`,
      `Patient: ${result.patient.name}, Age: ${result.patient.age||"N/A"}, Gender: ${result.patient.gender}`,
      `Urgency: ${result.diagnosis.overall_urgency.toUpperCase()}`,
      `Action: ${result.diagnosis.urgency_action}`,
      `Symptoms: ${symText}`,
      `Conditions: ${result.diagnosis.possible_conditions.map(c=>c.condition).join(", ")}`,
      `Systems: ${result.analysis.affected_systems.join(", ")}`,
      `Recommendations:\n${result.diagnosis.general_recommendations.map(r=>"• "+r).join("\n")}`,
      `\n⚠️ AI-generated. Not a substitute for medical advice.`,
    ];
    navigator.clipboard.writeText(lines.join("\n")).then(()=>{ setCopied(true); setTimeout(()=>setCopied(false),2000); });
  };

  return (
    <div className="diagnosis-result">
      {/* Urgency Banner */}
      <div className="urgency-banner" style={{background:urg.bg, borderColor:urg.border}}>
        <div className="urgency-left">
          <span className="urgency-icon">{urg.icon}</span>
          <div>
            <p className="urgency-level" style={{color:urg.color}}>{urg.label} URGENCY</p>
            <p className="urgency-action">{result.diagnosis.urgency_action}</p>
          </div>
        </div>
        <div className="urgency-actions">
          <button className="icon-btn" onClick={copyReport} title="Copy Report">{copied?"✔":"📋"}</button>
          <button className="icon-btn" onClick={onReset} title="New Patient">↩</button>
        </div>
      </div>

      {/* Patient + Recognition */}
      <div className="result-meta-row">
        <div className="meta-box">
          <span className="meta-icon">👤</span>
          <div>
            <p className="meta-title">{result.patient.name}</p>
            <p className="meta-sub">{result.patient.age ? `${result.patient.age} yrs` : "Age N/A"} · {result.patient.gender}</p>
          </div>
        </div>
        <div className="meta-box">
          <span className="meta-icon">🔍</span>
          <div>
            <p className="meta-title">{result.analysis.symptom_count} Symptoms</p>
            <p className="meta-sub">{result.analysis.recognition_rate}% recognized</p>
          </div>
        </div>
        <div className="meta-box">
          <span className="meta-icon">🏥</span>
          <div>
            <p className="meta-title">{result.analysis.affected_systems.length} System(s)</p>
            <p className="meta-sub">{result.analysis.affected_systems.slice(0,2).join(", ")}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// -- Conditions List --
function ConditionsList({ conditions }) {
  const max = conditions[0]?.mentions || 1;
  return (
    <div className="conditions-list">
      <h3 className="section-heading"><span>🩺</span> Possible Conditions</h3>
      {conditions.map((c,i)=>(
        <div key={i} className="condition-row">
          <div className="cond-rank">#{i+1}</div>
          <div className="cond-info">
            <span className="cond-name">{c.condition}</span>
            <div className="cond-bar-wrap">
              <div className="cond-bar" style={{width:`${(c.mentions/max)*100}%`}}/>
            </div>
          </div>
          <span className="cond-count">{c.mentions} signal{c.mentions>1?"s":""}</span>
        </div>
      ))}
    </div>
  );
}

// -- Symptoms Tags --
function SymptomTags({ recognized, entered }) {
  const enteredParts = entered.split(/[,;\n]/).map(s=>s.trim().toLowerCase()).filter(Boolean);
  return (
    <div className="symptoms-section">
      <h3 className="section-heading"><span>🔬</span> Symptom Recognition</h3>
      <div className="symptom-tags">
        {enteredParts.map((s,i)=>{
          const matched = recognized.some(r=>s.includes(r)||r.includes(s));
          return <span key={i} className={`symptom-tag ${matched?"matched":"unmatched"}`}>{s}</span>;
        })}
      </div>
      {recognized.length > 0 && (
        <p className="sym-note">✔ Matched: {recognized.join(" · ")}</p>
      )}
    </div>
  );
}

// -- Recommendations --
function Recommendations({ general, vital }) {
  const all = [...general, ...(vital||[])];
  return (
    <div className="recs-section">
      <h3 className="section-heading"><span>💊</span> Recommendations</h3>
      <ul className="recs-list">
        {all.map((r,i)=>(
          <li key={i} className="rec-item"><span className="rec-bullet">→</span>{r}</li>
        ))}
      </ul>
    </div>
  );
}

// -- History Panel --
function HistoryPanel({ records, onClear }) {
  if (!records.length) return (
    <div className="empty-state">
      <span className="empty-icon">📂</span>
      <p>No patient records yet</p>
    </div>
  );
  return (
    <div className="history-panel">
      <div className="history-header">
        <span>{records.length} Record{records.length>1?"s":""}</span>
        <button className="clear-btn" onClick={onClear}>Clear All</button>
      </div>
      {records.map(r=>{
        const urg = URGENCY[r.overall_urgency]||URGENCY.low;
        return (
          <div key={r.id} className="history-card">
            <div className="hc-left">
              <span className="hc-id">#{r.id}</span>
              <div>
                <p className="hc-name">{r.patient_name}</p>
                <p className="hc-meta">{r.age ? `${r.age}y` : "—"} · {r.gender} · {r.timestamp.split(" ")[1]}</p>
              </div>
            </div>
            <div className="hc-right">
              <span className="urgency-chip" style={{color:urg.color,borderColor:urg.border,background:urg.bg}}>
                {urg.icon} {urg.label}
              </span>
              <p className="hc-cond">{r.possible_conditions.slice(0,2).join(", ") || "—"}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}

// -- Stats Panel --
function StatsPanel({ stats }) {
  if(!stats||stats.total_patients===0) return (
    <div className="empty-state"><span className="empty-icon">📊</span><p>No data yet</p></div>
  );
  const urgColors = { critical:"#ef4444", high:"#f97316", medium:"#f59e0b", low:"#10b981" };
  return (
    <div className="stats-panel">
      <div className="stats-grid-top">
        {[
          {label:"Total Patients",  val:stats.total_patients,    icon:"👥"},
          {label:"Avg Age",         val:stats.average_age||"N/A",icon:"🎂"},
          {label:"Top Condition",   val:stats.top_conditions?.[0]?.condition||"—", icon:"🩺"},
          {label:"Dominant Urgency",val:stats.urgency_distribution ? Object.entries(stats.urgency_distribution).sort((a,b)=>b[1]-a[1])[0]?.[0]:"—", icon:"⚡"},
        ].map((s,i)=>(
          <div key={i} className="stat-card">
            <span className="stat-icon">{s.icon}</span>
            <span className="stat-big">{s.val}</span>
            <span className="stat-lbl">{s.label}</span>
          </div>
        ))}
      </div>
      {stats.urgency_distribution && (
        <div className="urgency-dist">
          <p className="dist-title">Urgency Distribution</p>
          {Object.entries(stats.urgency_distribution).map(([u,n])=>(
            <div key={u} className="dist-row">
              <span className="dist-label" style={{color:urgColors[u]||"#fff"}}>{u.toUpperCase()}</span>
              <div className="dist-bar-wrap">
                <div className="dist-bar" style={{width:`${(n/stats.total_patients)*100}%`,background:urgColors[u]}}/>
              </div>
              <span className="dist-num">{n}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// =============================================
//   MAIN APP
// =============================================
export default function App() {
  const [tab, setTab]           = useState("diagnose");
  const [form, setForm]         = useState({ patient_name:"", age:"", gender:"", notes:"" });
  const [symptoms, setSymptoms] = useState("");
  const [vitals, setVitals]     = useState({});
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);
  const [result, setResult]     = useState(null);
  const [history, setHistory]   = useState([]);
  const [statsData, setStats]   = useState(null);

  const TABS = [
    { id:"diagnose", label:"Diagnose",   icon:"🩺" },
    { id:"history",  label:"History",    icon:"📋" },
    { id:"stats",    label:"Statistics", icon:"📊" },
  ];

  const loadHistory = useCallback(async () => {
    try {
      const r = await fetch(`${API}/patients`);
      const d = await r.json();
      if(d.status==="success") setHistory(d.records);
    } catch {}
  },[]);

  const loadStats = useCallback(async () => {
    try {
      const r = await fetch(`${API}/stats`);
      const d = await r.json();
      if(d.status==="success") setStats(d);
    } catch {}
  },[]);

  useEffect(()=>{ if(tab==="history") loadHistory(); if(tab==="stats") loadStats(); },[tab,loadHistory,loadStats]);

  const handleDiagnose = async () => {
    if(!symptoms.trim()) return;
    setLoading(true); setError(null); setResult(null);
    try {
      const res = await fetch(`${API}/diagnose`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ ...form, symptoms, vitals }),
      });
      if(!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      if(data.error) throw new Error(data.error);
      setResult(data);
    } catch(e) {
      setError(e.message||"Connection failed. Make sure backend is running on port 5000.");
    } finally { setLoading(false); }
  };

  const handleReset = () => {
    setResult(null); setSymptoms(""); setVitals({}); setError(null);
    setForm({ patient_name:"", age:"", gender:"", notes:"" });
  };

  const handleClearHistory = async () => {
    await fetch(`${API}/patients`,{method:"DELETE"});
    setHistory([]);
  };

  const canSubmit = symptoms.trim().length>0 && !loading;

  return (
    <>
      <NeuralCanvas/>
      <div className="grid-overlay"/>
      <div className="blob blob-1"/><div className="blob blob-2"/><div className="blob blob-3"/>

      <div className="app-root">
        {/* HEADER */}
        <header className="app-header">
          <div className="header-brand">
            <div className="brand-icon">⚕</div>
            <div>
              <h1 className="app-title">Medi<span className="accent">Scope</span><span className="plus">+</span></h1>
              <p className="app-subtitle">AI-Powered Medical Analysis System</p>
            </div>
            <div className="header-right">
              <span className="live-badge"><span className="pulse-dot"/>LIVE</span>
            </div>
          </div>
          <div className="header-stats-row">
            {[
              {v:"50+",  l:"Symptoms"},
              {v:"6",    l:"Vital Signs"},
              {v:"4",    l:"Urgency Levels"},
              {v:"100+", l:"Conditions"},
            ].map((s,i)=>(
              <div key={i} className="hstat">
                <span className="hstat-v">{s.v}</span>
                <span className="hstat-l">{s.l}</span>
              </div>
            ))}
          </div>
        </header>

        {/* TABS */}
        <TabBar tabs={TABS} active={tab} onChange={setTab}/>

        {/* MAIN CARD */}
        <div className="glass-card">
          {/* DIAGNOSE TAB */}
          {tab==="diagnose" && !result && (
            <div className="diagnose-form">
              {/* Patient Info */}
              <div className="form-section">
                <h2 className="form-section-title"><span>👤</span> Patient Information</h2>
                <div className="patient-grid">
                  <div className="field-group">
                    <label className="field-label">PATIENT NAME</label>
                    <input className="neuro-input" placeholder="e.g. Ahmed Khan" value={form.patient_name}
                      onChange={e=>setForm(f=>({...f,patient_name:e.target.value}))}/>
                  </div>
                  <div className="field-group">
                    <label className="field-label">AGE</label>
                    <input className="neuro-input" type="number" placeholder="e.g. 35" value={form.age}
                      onChange={e=>setForm(f=>({...f,age:e.target.value}))}/>
                  </div>
                  <div className="field-group">
                    <label className="field-label">GENDER</label>
                    <select className="neuro-select" value={form.gender} onChange={e=>setForm(f=>({...f,gender:e.target.value}))}>
                      <option value="">Select</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Symptoms */}
              <div className="form-section">
                <h2 className="form-section-title"><span>🔬</span> Symptoms</h2>
                <div className="field-group">
                  <div className="field-top-row">
                    <label className="field-label">DESCRIBE SYMPTOMS</label>
                    <span className="field-hint">Separate with commas</span>
                  </div>
                  <textarea className="neuro-textarea" rows={4}
                    placeholder="e.g. chest pain, shortness of breath, fatigue, headache..."
                    value={symptoms} onChange={e=>setSymptoms(e.target.value)}/>
                </div>
                <div className="quick-symptoms">
                  <p className="quick-label">Quick add:</p>
                  {["fever","headache","cough","fatigue","chest pain","nausea","dizziness","back pain"].map(s=>(
                    <button key={s} className="quick-tag" onClick={()=>setSymptoms(p=>p ? p+", "+s : s)}>{s}</button>
                  ))}
                </div>
              </div>

              {/* Vitals */}
              <div className="form-section">
                <h2 className="form-section-title"><span>📊</span> Vital Signs <span className="optional-tag">Optional</span></h2>
                <VitalsPanel vitals={vitals} setVitals={setVitals}/>
              </div>

              {/* Notes */}
              <div className="form-section">
                <h2 className="form-section-title"><span>📝</span> Clinical Notes <span className="optional-tag">Optional</span></h2>
                <textarea className="neuro-textarea" rows={2}
                  placeholder="Any additional notes, medical history, current medications..."
                  value={form.notes} onChange={e=>setForm(f=>({...f,notes:e.target.value}))}/>
              </div>

              {/* Error */}
              {error && (
                <div className="error-card">
                  <span>⚠️</span>
                  <div><p className="error-title">Error</p><p className="error-msg">{error}</p></div>
                </div>
              )}

              {/* Submit */}
              <button className="submit-btn" onClick={handleDiagnose} disabled={!canSubmit}>
                <span className="btn-shine"/>
                <span className="btn-content">
                  {loading ? <><span className="spinner"/>Analyzing Patient Data...</> : <><span>⚡</span> Run Medical Analysis</>}
                </span>
              </button>

              <p className="disclaimer">⚠️ AI-generated results for educational purposes only. Not a substitute for professional medical advice.</p>
            </div>
          )}

          {/* RESULT */}
          {tab==="diagnose" && result && (
            <div className="result-view">
              <DiagnosisResult result={result} onReset={handleReset}/>
              <VitalsResult items={result.vitals_analysis}/>
              <ConditionsList conditions={result.diagnosis.possible_conditions}/>
              <SymptomTags recognized={result.analysis.symptoms_recognized} entered={result.analysis.symptoms_entered}/>
              <Recommendations general={result.diagnosis.general_recommendations} vital={result.diagnosis.vital_recommendations}/>
              {result.notes && <div className="notes-box"><span>📝</span> {result.notes}</div>}
              <button className="submit-btn secondary" onClick={handleReset}>
                <span className="btn-content"><span>+</span> New Patient Analysis</span>
              </button>
            </div>
          )}

          {/* HISTORY TAB */}
          {tab==="history" && <HistoryPanel records={history} onClear={handleClearHistory}/>}

          {/* STATS TAB */}
          {tab==="stats" && <StatsPanel stats={statsData}/>}
        </div>

        <footer className="app-footer">
          <span>MediScope+ © 2026</span><span className="footer-dot">·</span>
          <span>AI Medical Assistant</span><span className="footer-dot">·</span>
          <span>🔒 Encrypted</span>
        </footer>
      </div>
    </>
  );
}

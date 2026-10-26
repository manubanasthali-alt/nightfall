from flask import Flask, jsonify, render_template_string
import psutil
import platform
import time
import random
import os

app = Flask(__name__)
START_TIME = time.time()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PROJECT NIGHTFALL | CYBER OPS</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#050b12;color:#d9faff;font-family:Arial,sans-serif}
header{padding:22px 16px;border-bottom:1px solid #00e5ff55;background:#081521}
h1{margin:0;color:#00e5ff;letter-spacing:3px;font-size:clamp(22px,4vw,36px)}
.sub{color:#7b9eac;margin-top:8px;font-size:12px;letter-spacing:2px}
main{padding:16px;max-width:1200px;margin:auto}
.status{color:#64ffb2;font-size:13px;margin:18px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.card{background:#0a1722;border:1px solid #174452;border-radius:10px;padding:18px;box-shadow:0 0 18px #00e5ff08}
.label{color:#7b9eac;font-size:12px;letter-spacing:1.5px}
.value{font-size:32px;color:#00e5ff;margin:14px 0}
.bar{height:7px;background:#152a36;border-radius:5px;overflow:hidden}
.fill{height:100%;width:0;background:#00e5ff;transition:width .5s}
.section{margin-top:18px}
h2{font-size:15px;color:#64ffb2;letter-spacing:2px}
canvas{width:100%;height:180px;background:#07121c;border:1px solid #174452;border-radius:8px}
.log{font-family:monospace;font-size:12px;line-height:1.9;color:#a4c5d0;overflow-wrap:anywhere}
footer{color:#587786;font-size:11px;text-align:center;padding:25px}
.badge{display:inline-block;border:1px solid #64ffb2;padding:5px 8px;color:#64ffb2;border-radius:4px;font-size:11px}
</style>
</head>
<body>
<header>
<h1>PROJECT NIGHTFALL</h1>
<div class="sub">CYBER OPERATIONS DASHBOARD // SYSTEM MONITOR</div>
</header>
<main>
<div class="status">● SYSTEM ONLINE <span class="badge">MONITORING</span></div>
<div class="grid">
<div class="card"><div class="label">CPU USAGE</div><div class="value" id="cpu">--%</div><div class="bar"><div class="fill" id="cpubar"></div></div></div>
<div class="card"><div class="label">RAM USAGE</div><div class="value" id="ram">--%</div><div class="bar"><div class="fill" id="rambar"></div></div></div>
<div class="card"><div class="label">SYSTEM UPTIME</div><div class="value" id="uptime">--</div><div class="label">SERVER RUNNING TIME</div></div>
<div class="card"><div class="label">PLATFORM</div><div class="value" style="font-size:21px" id="platform">--</div><div class="label">SERVER HOST</div></div>
</div>
<div class="section card">
<h2>LIVE RESOURCE GRAPH</h2>
<canvas id="graph" width="1000" height="180"></canvas>
</div>
<div class="section card">
<h2>SECURITY EVENT FEED</h2>
<div class="log" id="logs">[INFO] Dashboard initialized<br>[INFO] Live system monitoring starting...</div>
</div>
<div class="section card">
<h2>DEMO RADAR</h2>
<canvas id="radar" width="500" height="300"></canvas>
<div class="log">VISUAL SIMULATION ONLY — This radar does not scan networks or detect real threats.</div>
</div>
</main>
<footer>PROJECT NIGHTFALL // Authorized system monitoring only</footer>
<script>
const $=id=>document.getElementById(id);
let history=[],events=[];
async function update(){
 try{
  const r=await fetch('/api/status');
  const d=await r.json();
  $('cpu').textContent=d.cpu+'%';
  $('ram').textContent=d.ram+'%';
  $('uptime').textContent=d.uptime;
  $('platform').textContent=d.platform;
  $('cpubar').style.width=d.cpu+'%';
  $('rambar').style.width=d.ram+'%';
  history.push(d.cpu);if(history.length>70)history.shift();
  drawGraph();
  if(Math.random()<0.35){
   const messages=['System metrics refreshed','Resource monitor healthy','Monitoring service active','No automated threat scan performed'];
   events.unshift(new Date().toLocaleTimeString()+'  [INFO] '+messages[Math.floor(Math.random()*messages.length)]);
   events=events.slice(0,8);
   $('logs').innerHTML=events.map(e=>e.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')).join('<br>');
  }
 }catch(e){}
}
function drawGraph(){
 const c=$('graph'),x=c.getContext('2d'),w=c.width,h=c.height;
 x.clearRect(0,0,w,h);x.strokeStyle='#15303b';x.lineWidth=1;
 for(let i=1;i<5;i++){x.beginPath();x.moveTo(0,h*i/5);x.lineTo(w,h*i/5);x.stroke()}
 x.strokeStyle='#00e5ff';x.lineWidth=3;x.beginPath();
 history.forEach((v,i)=>{let px=i/(Math.max(69,history.length-1))*w,py=h-(v/100)*h;if(i===0)x.moveTo(px,py);else x.lineTo(px,py)});
 x.stroke();
}
function drawRadar(){
 const c=$('radar'),x=c.getContext('2d'),w=c.width,h=c.height;
 x.clearRect(0,0,w,h);const cx=w/2,cy=h/2,r=Math.min(w,h)*.42;
 x.strokeStyle='#164b4c';x.lineWidth=1;
 for(let i=1;i<=4;i++){x.beginPath();x.arc(cx,cy,r*i/4,0,Math.PI*2);x.stroke()}
 x.beginPath();x.moveTo(cx-r,cy);x.lineTo(cx+r,cy);x.moveTo(cx,cy-r);x.lineTo(cx,cy+r);x.stroke();
 let a=Date.now()/1200;
 x.strokeStyle='#64ffb2';x.beginPath();x.moveTo(cx,cy);x.lineTo(cx+Math.cos(a)*r,cy+Math.sin(a)*r);x.stroke();
 requestAnimationFrame(drawRadar);
}
drawRadar();update();setInterval(update,2000);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/status")
def status():
    mem = psutil.virtual_memory()
    elapsed = int(time.time() - START_TIME)
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    return jsonify({
        "cpu": "N/A",
        "ram": mem.percent,
        "uptime": f"{hours:02}:{minutes:02}:{seconds:02}",
        "platform": platform.system() + " " + platform.machine()
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

#!/usr/bin/env python3
"""Render a recorded plant CSV as a standalone offline HTML viewer; no live I/O."""
import argparse
import csv
import json
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('csv',type=Path)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
with a.csv.open() as f:
    rows=[{k:int(v) for k,v in row.items()} for row in csv.DictReader(f)]
if not rows: raise SystemExit('Empty trace')
required={'ms','volume_ml','p1_run','p2_run','high_alarm','invalid_alarm','no_pump_alarm'}
if not required.issubset(rows[0]): raise SystemExit('Not a plant trace: missing columns')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Recorded PLC teaching trace</title><style>
body{font:18px system-ui;margin:0;background:#f5f1e8;color:#162e35}main{max-width:1050px;margin:auto;padding:32px}h1{font-size:36px;margin-bottom:8px}.note{max-width:78ch;line-height:1.5}canvas{width:100%;height:300px;background:white;border:2px solid #162e35}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}.card{padding:18px;border:2px solid #162e35;background:white}.value{font-size:26px;font-weight:bold}input{width:100%}button{font:inherit;padding:8px 14px;background:#162e35;color:white;border:0;cursor:pointer}pre{white-space:pre-wrap;background:white;padding:15px}label{display:block;margin:22px 0 8px}small{display:block;margin-top:12px} .on{background:#d0ecda}.alarm{background:#ffceba}</style>
<main><h1>Duplex station • recorded trace</h1><p class="note">Actual compiled Structured Text commands, coupled to a Python toy wet well. This is an offline replay of saved evidence. The slider changes the displayed scan only. No hardware, live control, network connection or production-runtime claim.</p>
<canvas id="chart" width="1000" height="300" aria-label="Recorded volume versus time"></canvas>
<label for="scan">Inspect scan <strong id="time"></strong></label><input id="scan" type="range" min="0" value="0" step="1"><p><button id="back">Previous scan</button> <button id="next">Next scan</button></p><div id="cards" class="grid"></div><h2>Exact input/output row</h2><pre id="row"></pre><small>Volume is sampled before this scan's outflow update. Orange reference line: high-level threshold (85 L). Values and flows are invented teaching quantities.</small></main>
<script>const rows=__DATA__;const slider=document.getElementById('scan');slider.max=rows.length-1;const canvas=document.getElementById('chart'),ctx=canvas.getContext('2d');
function draw(){const i=+slider.value,r=rows[i],w=canvas.width,h=canvas.height;ctx.clearRect(0,0,w,h);ctx.strokeStyle='#a94518';ctx.setLineDash([6,6]);ctx.beginPath();ctx.moveTo(45,25+(1-.85)*230);ctx.lineTo(w-15,25+(1-.85)*230);ctx.stroke();ctx.setLineDash([]);ctx.strokeStyle='#14706a';ctx.lineWidth=2;ctx.beginPath();rows.forEach((p,k)=>{const x=45+k/(rows.length-1)*(w-60),y=25+(1-p.volume_ml/100000)*230;k?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke();ctx.strokeStyle='#162e35';const x=45+i/(rows.length-1)*(w-60);ctx.beginPath();ctx.moveTo(x,15);ctx.lineTo(x,260);ctx.stroke();ctx.fillStyle='#162e35';ctx.font='15px system-ui';ctx.fillText('100 L',0,25);ctx.fillText('0 L',12,260);ctx.fillText('0 s',45,285);ctx.fillText((rows.at(-1).ms/1000)+' s',w-70,285);document.getElementById('time').textContent=i+' · '+(r.ms/1000).toFixed(1)+' s';
const fields=[['Volume',(r.volume_ml/1000).toFixed(2)+' L',''],['Pump 1 command',r.p1_run?'ON':'OFF',r.p1_run?'on':''],['Pump 2 command',r.p2_run?'ON':'OFF',r.p2_run?'on':''],['Lead',r.lead,''],['High level',r.high_alarm?'ALARM':'clear',r.high_alarm?'alarm':''],['Float consistency',r.invalid_alarm?'INVALID':'consistent',r.invalid_alarm?'alarm':''],['Availability',r.no_pump_alarm?'NO PUMP':'no alarm',r.no_pump_alarm?'alarm':'']];const cards=document.getElementById('cards');cards.replaceChildren();for(const [label,value,cl] of fields){const box=document.createElement('div');box.className='card '+cl;const title=document.createElement('div');title.textContent=label;const val=document.createElement('div');val.className='value';val.textContent=value;box.append(title,val);cards.append(box)}document.getElementById('row').textContent=JSON.stringify(r,null,2)}
slider.addEventListener('input',draw);document.getElementById('back').onclick=()=>{slider.value=Math.max(0,+slider.value-1);draw()};document.getElementById('next').onclick=()=>{slider.value=Math.min(rows.length-1,+slider.value+1);draw()};draw();</script></html>'''
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(html.replace('__DATA__',json.dumps(rows,separators=(',',':')).replace('<','\\u003c')))
print('Offline trace viewer:',a.output.resolve())

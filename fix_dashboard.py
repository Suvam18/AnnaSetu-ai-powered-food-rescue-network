content = open('Restaurant_Portal_Dashboard.html','r',encoding='utf-8').read()

# Cut at the comment or at </main> — keep all HTML, replace only the script block
cut_marker = '<!-- BottomNavBar (Mobile) -->'
idx = content.find(cut_marker)
if idx != -1:
    base = content[:idx]
else:
    # fallback: cut after last </main>
    idx = content.rfind('</main>')
    base = content[:idx+len('</main>')]

new_tail = '''
<script>
/* ═══════════════════════════════════════════════════
   SHARED DATA — same localStorage keys as Surplus Log
   annasetu_surplus  : active surplus entries
   annasetu_history  : rescued history
   annasetu_branches : restaurant branches
═══════════════════════════════════════════════════ */
function getSurplus()  { try{ return JSON.parse(localStorage.getItem('annasetu_surplus') ||'[]'); }catch(e){ return []; } }
function getHistory()  { try{ return JSON.parse(localStorage.getItem('annasetu_history') ||'[]'); }catch(e){ return []; } }
function getBranches() {
    const def = [{ id:1, name:'Main Branch', address:'City Centre', icon:'restaurant' }];
    try{ return JSON.parse(localStorage.getItem('annasetu_branches') || JSON.stringify(def)); }catch(e){ return def; }
}
function saveBranchesData(arr) { localStorage.setItem('annasetu_branches', JSON.stringify(arr)); }

/* ─── BRANCH ACTIONS — must be global for onclick= ─── */
function openAddBranch() {
    document.getElementById('add-branch-form').classList.remove('hidden');
    document.getElementById('branch-name').focus();
}
function closeAddBranch() {
    document.getElementById('add-branch-form').classList.add('hidden');
    document.getElementById('branch-name').value = '';
    document.getElementById('branch-address').value = '';
}
function saveBranch() {
    const name    = document.getElementById('branch-name').value.trim();
    const address = document.getElementById('branch-address').value.trim();
    const icon    = document.getElementById('branch-icon').value;
    if (!name) { document.getElementById('branch-name').classList.add('border-red-400'); return; }
    document.getElementById('branch-name').classList.remove('border-red-400');
    const branches = getBranches();
    branches.push({ id: Date.now(), name, address: address || 'No address', icon });
    saveBranchesData(branches);
    closeAddBranch();
    renderBranches();
}
function deleteBranch(id, evt) {
    evt.stopPropagation();
    if (!confirm('Remove this branch?')) return;
    saveBranchesData(getBranches().filter(function(b){ return b.id !== id; }));
    renderBranches();
}

/* ─── RENDER BRANCHES (also shows today surplus per branch) ─── */
function renderBranches() {
    var branches = getBranches();
    var list = document.getElementById('branches-list');
    if (!list) return;
    list.innerHTML = '';
    if (branches.length === 0) {
        list.innerHTML = '<p class="text-xs text-stone-400 text-center py-4">No branches yet. Click Add!</p>';
        return;
    }
    var surplus = getSurplus();
    var now = new Date();
    var todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    branches.forEach(function(b) {
        var todayMeals = surplus
            .filter(function(e){ var d=new Date(e.createdAt); return d>=todayStart && (e.branchId===b.id || !e.branchId); })
            .reduce(function(s,e){ return s+(parseInt(e.qty)||0); }, 0);
        var active = todayMeals > 0;
        var row = document.createElement('div');
        row.className = 'flex items-center gap-3 p-3 hover:bg-stone-50 rounded-xl transition-colors group';
        row.innerHTML =
            '<div class="w-11 h-11 rounded-xl bg-stone-100 flex items-center justify-center text-stone-400 group-hover:bg-emerald-50 group-hover:text-[#4a7c59] transition-colors shrink-0">' +
                '<span class="material-symbols-outlined text-xl">' + b.icon + '</span>' +
            '</div>' +
            '<div class="flex-1 min-w-0">' +
                '<h4 class="font-bold text-on-surface text-sm truncate">' + b.name + '</h4>' +
                '<p class="text-xs text-stone-400 truncate">' + b.address + '</p>' +
            '</div>' +
            '<div class="flex flex-col items-end gap-1 shrink-0">' +
                '<span class="text-xs font-black ' + (active ? 'text-[#4a7c59]' : 'text-stone-400') + '">' + (todayMeals > 0 ? todayMeals + ' meals' : '0 today') + '</span>' +
                '<span class="w-2 h-2 rounded-full ' + (active ? 'bg-emerald-500' : 'bg-stone-300') + '"></span>' +
            '</div>' +
            '<button onclick="deleteBranch(' + b.id + ',event)" class="ml-1 p-1 text-stone-300 hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100">' +
                '<span class="material-symbols-outlined text-sm">delete</span>' +
            '</button>';
        list.appendChild(row);
    });
}

/* ─── CHARTS ─── */
var CHART_COLORS = { 'Bakery':'#4a7c59','Produce':'#3b82f6','Prepared Meals':'#f59e0b','Beverages':'#8b5cf6','Other':'#94a3b8' };

function renderTrendChart() {
    var rangeEl = document.getElementById('trend-range');
    if (!rangeEl) return;
    var range = parseInt(rangeEl.value);
    var surplus = getSurplus();
    var history = getHistory();
    var allEntries = surplus.map(function(e){ return { date:new Date(e.createdAt), qty:parseInt(e.qty)||0, type:e.foodType||'Other' }; })
        .concat(history.map(function(h){ return { date:new Date(h.createdAt||h.date||Date.now()), qty:parseInt(h.qty)||0, type:h.type||'Other' }; }));
    var now = new Date();
    var labels=[], data=[];

    if (range===12) {
        var months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        labels=months;
        data=months.map(function(_,mi){ return allEntries.filter(function(e){ return e.date.getFullYear()===now.getFullYear()&&e.date.getMonth()===mi; }).reduce(function(s,e){ return s+e.qty; },0); });
        document.getElementById('chart-subtitle').textContent='This year · monthly breakdown';
    } else {
        for(var i=range-1;i>=0;i--){
            var day=new Date(now); day.setDate(now.getDate()-i); day.setHours(0,0,0,0);
            var end=new Date(day); end.setHours(23,59,59,999);
            data.push(allEntries.filter(function(e){ return e.date>=day&&e.date<=end; }).reduce(function(s,e){ return s+e.qty; },0));
            labels.push(range===7?['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][day.getDay()]:day.getDate().toString());
        }
        document.getElementById('chart-subtitle').textContent='Last '+range+' days · from your entries';
    }

    var maxVal=Math.max.apply(null,data.concat([1]));
    var total=data.reduce(function(s,v){ return s+v; },0);
    var chartEl=document.getElementById('trend-chart');
    var emptyEl=document.getElementById('chart-empty');

    // BAR CHART
    if(total===0){
        chartEl.innerHTML=''; emptyEl.classList.remove('hidden');
        document.getElementById('trend-summary').textContent='No data yet — add entries in Surplus Log!';
        document.getElementById('trend-total').textContent='';
    } else {
        emptyEl.classList.add('hidden'); chartEl.innerHTML='';
        var todayIdx=range===12?now.getMonth():range-1;
        data.forEach(function(val,i){
            var pct=Math.max(4,Math.round((val/maxVal)*100));
            var isToday=i===todayIdx;
            var col=document.createElement('div');
            col.className='flex flex-col items-center flex-1 gap-1 min-w-0 group cursor-default';
            var clr=isToday?'bg-[#4a7c59]':val>maxVal*0.7?'bg-[#4a7c59]/80':'bg-[#4a7c59]/40';
            var labelClr=isToday?'text-[#4a7c59]':'text-stone-400';
            col.innerHTML='<div class="relative w-full flex flex-col items-center">'+(val>0?'<span class="text-[8px] font-bold text-[#4a7c59] mb-0.5 opacity-0 group-hover:opacity-100 transition-opacity">'+val+'</span>':'')+'<div class="w-full '+clr+' rounded-t-md transition-all duration-500" style="height:'+pct+'%" title="'+val+' meals"></div></div><span class="text-[8px] font-bold truncate w-full text-center '+labelClr+'">'+labels[i]+'</span>';
            chartEl.appendChild(col);
        });
        var half=Math.floor(data.length/2);
        var prev=data.slice(0,half).reduce(function(s,v){ return s+v; },0);
        var next=data.slice(half).reduce(function(s,v){ return s+v; },0);
        var ico=document.getElementById('trend-icon'); var sumEl=document.getElementById('trend-summary');
        if(next>=prev){ ico.textContent='trending_up'; ico.className='material-symbols-outlined text-lg text-emerald-600'; sumEl.textContent='Trending up \u2191 \u00b7 '+total+' meals total'; sumEl.className='text-emerald-700 font-bold'; }
        else { ico.textContent='trending_down'; ico.className='material-symbols-outlined text-lg text-amber-500'; sumEl.textContent='Slight dip \u2014 keep donating! ('+total+' meals)'; sumEl.className='text-amber-600 font-bold'; }
        document.getElementById('trend-total').textContent='Peak: '+maxVal+' meals';
    }

    // PIE CHART
    var catTotals={};
    allEntries.forEach(function(e){ catTotals[e.type]=(catTotals[e.type]||0)+e.qty; });
    var cats=Object.entries(catTotals).filter(function(kv){ return kv[1]>0; }).sort(function(a,b){ return b[1]-a[1]; });
    var pieTotal=cats.reduce(function(s,kv){ return s+kv[1]; },0);
    var pieSvg=document.getElementById('pie-chart');
    var pieEmpty=document.getElementById('pie-empty');
    var legend=document.getElementById('pie-legend');
    document.getElementById('pie-center-value').textContent=pieTotal||0;
    pieSvg.querySelectorAll('.pie-seg').forEach(function(el){ el.remove(); });
    legend.innerHTML='';
    if(pieTotal===0){
        pieEmpty.classList.remove('hidden');
        legend.innerHTML='<p class="text-xs text-stone-400 italic">Add entries to see breakdown</p>';
    } else {
        pieEmpty.classList.add('hidden');
        var cx=60,cy=60,r=46,angle=-Math.PI/2;
        var donut=pieSvg.querySelector('circle:last-of-type');
        cats.forEach(function(kv){
            var cat=kv[0],val=kv[1];
            var slice=(val/pieTotal)*2*Math.PI;
            var x1=cx+r*Math.cos(angle),y1=cy+r*Math.sin(angle);
            var x2=cx+r*Math.cos(angle+slice),y2=cy+r*Math.sin(angle+slice);
            var large=slice>Math.PI?1:0;
            var color=CHART_COLORS[cat]||CHART_COLORS['Other'];
            var path=document.createElementNS('http://www.w3.org/2000/svg','path');
            path.setAttribute('class','pie-seg');
            path.setAttribute('d','M'+cx+','+cy+' L'+x1+','+y1+' A'+r+','+r+' 0 '+large+',1 '+x2+','+y2+' Z');
            path.setAttribute('fill',color); path.setAttribute('stroke','white'); path.setAttribute('stroke-width','2');
            path.style.transformOrigin='60px 60px'; path.style.transition='transform 0.2s';
            path.addEventListener('mouseenter',function(){ path.style.transform='scale(1.06)'; });
            path.addEventListener('mouseleave',function(){ path.style.transform=''; });
            pieSvg.insertBefore(path,donut);
            angle+=slice;
            var pct=Math.round((val/pieTotal)*100);
            var li=document.createElement('div'); li.className='flex items-center gap-2 min-w-0';
            li.innerHTML='<span class="w-2.5 h-2.5 rounded-full shrink-0" style="background:'+color+'"></span><span class="text-xs font-semibold text-stone-600 truncate">'+cat+'</span><span class="text-xs font-black ml-auto text-stone-800">'+pct+'%</span>';
            legend.appendChild(li);
        });
    }
}

/* ─── SUMMARY CARDS + ALERTS ─── */
function loadDashboardStats() {
    var surplus=getSurplus(), history=getHistory();
    var now=new Date(), todayStart=new Date(now.getFullYear(),now.getMonth(),now.getDate());
    var todayEntries=surplus.filter(function(e){ return new Date(e.createdAt)>=todayStart; });
    var totalToday=todayEntries.reduce(function(s,e){ return s+(parseInt(e.qty)||0); },0);
    var pendingCount=surplus.length;
    var todayLabel=now.toLocaleDateString('en-IN',{day:'numeric',month:'short'});
    var todayHist=history.filter(function(h){ return h.date===todayLabel; });
    var pickupsDone=todayHist.reduce(function(s,h){ return s+(parseInt(h.qty)||1); },0);
    var wasteSaved=Math.round((totalToday+pickupsDone)*0.25*10)/10;

    var el;
    if((el=document.getElementById('stat-surplus'))) el.textContent=totalToday||25;
    if((el=document.getElementById('stat-pickups'))) el.textContent=pickupsDone||18;
    if((el=document.getElementById('stat-pending'))) el.textContent=pendingCount||2;
    if((el=document.getElementById('stat-waste')))   el.innerHTML=(wasteSaved||12)+' <span class="text-lg font-semibold">kg</span>';
    if((el=document.getElementById('active-routes'))) el.textContent=Math.max(1,Math.min(pendingCount,5));

    // Urgent Alerts
    var alertsList=document.getElementById('alerts-list'), alertBadge=document.getElementById('alert-badge');
    var urgent=surplus.filter(function(e){ if(!e.expiry)return false; var d=(new Date(e.expiry)-Date.now())/60000; return d>0&&d<60; }).sort(function(a,b){ return new Date(a.expiry)-new Date(b.expiry); });
    if(alertBadge){ alertBadge.textContent=urgent.length; alertBadge.className=urgent.length>0?'text-xs bg-red-50 text-red-500 border border-red-100 font-bold px-2 py-0.5 rounded-full':'text-xs bg-stone-100 text-stone-400 border border-stone-200 font-bold px-2 py-0.5 rounded-full'; }
    if(alertsList){
        alertsList.innerHTML='';
        if(urgent.length===0){
            alertsList.innerHTML='<div class="flex items-center gap-3 p-3 bg-stone-50 rounded-xl text-stone-400 text-sm"><span class="material-symbols-outlined text-xl">check_circle</span><span>No urgent alerts right now.</span></div>';
        } else {
            urgent.slice(0,4).forEach(function(e){
                var diff=Math.round((new Date(e.expiry)-Date.now())/60000), ic=diff<30;
                var d=document.createElement('div');
                d.className='flex items-start gap-3 p-3 rounded-xl border-l-4 '+(ic?'bg-red-50 border-red-400':'bg-amber-50 border-amber-400');
                d.innerHTML='<span class="material-symbols-outlined '+(ic?'text-red-500':'text-amber-500')+' text-xl mt-0.5" style="font-variation-settings:\'FILL\' 1;">warning</span><div><p class="text-xs font-bold '+(ic?'text-red-600':'text-amber-600')+'">'+(ic?'\uD83D\uDD34 CRITICAL':'\uD83D\uDFE0 URGENT')+' \u2014 '+diff+'min left</p><p class="text-sm font-bold text-stone-800">'+e.qty+' meals \u00b7 '+e.foodType+'</p>'+(e.notes?'<p class="text-xs text-stone-500 italic">'+e.notes+'</p>':'')+'</div>';
                alertsList.appendChild(d);
            });
        }
    }
}

/* ─── INIT ─── */
document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle
    var btn=document.getElementById('theme-toggle');
    if(btn){ btn.addEventListener('click',function(){ var html=document.documentElement; html.classList.toggle('dark'); html.classList.toggle('light'); document.getElementById('theme-icon').textContent=html.classList.contains('dark')?'light_mode':'dark_mode'; html.style.backgroundColor=html.classList.contains('dark')?'#111':''; }); }

    // Dynamic greeting with restaurant name from session
    var grEl=document.getElementById('dashboard-greeting');
    if(grEl){
        var h=new Date().getHours();
        var greeting=h<12?'Good Morning \uD83C\uDF05':h<17?'Good Afternoon \u2600\uFE0F':'Good Evening \uD83C\uDF07';
        var name='';
        try{ var s=JSON.parse(localStorage.getItem('annasetu_session')||'{}'); name=s.fname||s.name||''; }catch(_){}
        if(name){ var parts=greeting.split(' '); grEl.textContent=parts[0]+' '+parts[1]+', '+name+'! '+parts[2]; }
        else { grEl.textContent=greeting; }
    }

    renderTrendChart();
    renderBranches();
    loadDashboardStats();

    // Auto-refresh every 30s (syncs with Surplus Log changes)
    setInterval(function(){ loadDashboardStats(); renderTrendChart(); renderBranches(); }, 30000);

    // Instant refresh when user switches back to this tab from Surplus Log
    document.addEventListener('visibilitychange', function(){ if(!document.hidden){ loadDashboardStats(); renderTrendChart(); renderBranches(); } });
});
</script>
</div>
</div>
</body></html>
'''

content = base + new_tail
open('Restaurant_Portal_Dashboard.html','w',encoding='utf-8').write(content)
print('Done. Lines:', content.count('\n'))

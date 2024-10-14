async function p(){try{const l=await(await fetch("/api/students")).json(),a={};l.forEach(t=>{a[t.coach]||(a[t.coach]=[]),a[t.coach].push(t)});const n=document.getElementById("coachesAccordion");n.innerHTML="",Object.keys(a).forEach((t,d)=>{const r=a[t],h=r.length,e=document.createElement("div");e.className="accordion-item";const i=`heading${d}`,o=`collapse${d}`;e.innerHTML=`
        <h2 class="accordion-header" id="${i}">
          <button class="accordion-button d-flex justify-content-between align-items-center" type="button" data-bs-toggle="collapse" data-bs-target="#${o}" aria-expanded="true" aria-controls="${o}" style="font-size: 24px;">
            <span class="text-primary fw-bold">${t} 教練</span>
            <span class="text-primary fw-bold ms-auto">學員數量: ${h}</span>
          </button>
        </h2>
        <div id="${o}" class="accordion-collapse collapse show" aria-labelledby="${i}">
          <div class="accordion-body">
            <table class="table">
              <thead>
                <tr>
                  <th>開始日期</th>
                  <th>學員名稱</th>
                  <th>狀態</th>
                </tr>
              </thead>
              <tbody>
                ${r.map(c=>`
                  <tr>
                    <td>${c.start_date||"未開始"}</td>
                    <td>${c.name}</td>
                    <td>${c.status}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      `,n.appendChild(e)})}catch(s){console.error("Error fetching student data:",s)}}p();

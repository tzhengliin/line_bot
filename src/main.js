// Fetch student data from the backend and render it on the page
async function fetchAndRenderStudents() {
    try {
        const response = await fetch('/api/students');
        const students = await response.json();

        // Group students by coach
        const coaches = {};
        students.forEach(student => {
            if (!coaches[student.coach]) {
                coaches[student.coach] = [];
            }
            coaches[student.coach].push(student);
        });

        // Get the accordion container
        const accordionContainer = document.getElementById('coachesAccordion');
        accordionContainer.innerHTML = ''; // Clear existing content

        // Render each coach and their students
        Object.keys(coaches).forEach((coach, index) => {
            const students = coaches[coach];
            const studentCount = students.length;

            // Create accordion item for each coach
            const accordionItem = document.createElement('div');
            accordionItem.className = 'accordion-item';

            const headerId = `heading${index}`;
            const collapseId = `collapse${index}`;

            accordionItem.innerHTML = `
        <h2 class="accordion-header" id="${headerId}">
          <button class="accordion-button d-flex justify-content-between align-items-center" type="button" data-bs-toggle="collapse" data-bs-target="#${collapseId}" aria-expanded="true" aria-controls="${collapseId}" style="font-size: 24px;">
            <span class="text-primary fw-bold">${coach} 教練</span>
            <span class="text-primary fw-bold ms-auto">學員數量: ${studentCount}</span>
          </button>
        </h2>
        <div id="${collapseId}" class="accordion-collapse collapse show" aria-labelledby="${headerId}">
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
                ${students.map(student => `
                  <tr>
                    <td>${student.start_date || '未開始'}</td>
                    <td>${student.name}</td>
                    <td>${student.status}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      `;

            accordionContainer.appendChild(accordionItem);
        });
    } catch (error) {
        console.error('Error fetching student data:', error);
    }
}

// Call the function to fetch and render students
fetchAndRenderStudents();


result = []
let datalength = 0
out = document.getElementById("datatobackend")
let students = []
fetch("datatopage", {
    method: 'GET',
})
    .then(response => response.json())
    .then(data => {
        students = data.output
        datalength = students.length
        console.log(students)
        renderStudents()

    });


out.onclick = function () {

    const jsonData = JSON.stringify(students);
    url = "updateattendence"

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',

        },
        body: jsonData,
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)

        });




}
function renderStudents() {

    const tableBody = document.getElementById("tableBody");
    if (!tableBody) return;


    tableBody.innerHTML = "";


    students.forEach(student => {
        const row = tableBody.insertRow();
        const usnCell = row.insertCell(0);

        const actionCell = row.insertCell(1);

        usnCell.textContent = student.student;


        const select = document.createElement("select");
        select.innerHTML = "<option value=''>Select</option><option value='Present'>Present</option><option value='Absent'>Absent</option>";


        actionCell.appendChild(select);
        select.addEventListener("change", (event) => markAttendance(student, event.target.value));

    });
}



function markAttendance(student, status) {

    student.status = status;
    stu = student.student
    students.forEach(studentdata => {
        if (studentdata.student == stu) {
            studentdata.status = status
        }
    })



}



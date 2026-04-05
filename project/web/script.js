/* ДОБАВЛЯЕМ АДМИНА АВТО */
(function() {
    let users = JSON.parse(localStorage.getItem("users") || "[]");

    let exists = users.find(u => u.email === "user614362");

    if (!exists) {
        users.push({
            name: "fol",
            email: "user614362",
            password: "ppjquc",
            is_admin: 1
        });

        localStorage.setItem("users", JSON.stringify(users));
    }
})();
<script>
window.onload = () => {

    let tg = window.Telegram.WebApp;
    tg.expand();

    // ⚠️ временно всегда админ (чтобы кнопка точно была)
    let isAdmin = true;

    let API = "http://127.0.0.1:5000";

    // создаём контейнер если нет
    let container = document.getElementById("courses");
    if (!container) {
        container = document.createElement("div");
        container.id = "courses";
        document.body.appendChild(container);
    }

    // кнопка админ панели
    if (isAdmin) {
        let btn = document.createElement("button");
        btn.innerText = "⚙️ Админ панель";
        btn.style.padding = "10px";
        btn.style.margin = "10px";
        btn.onclick = openAdmin;
        document.body.prepend(btn);
    }

    // загрузка курсов
    async function loadCourses() {
        try {
            let res = await fetch(API + "/courses");
            let courses = await res.json();

            container.innerHTML = "";

            courses.forEach(course => {
                let div = document.createElement("div");
                div.style.border = "1px solid #ccc";
                div.style.padding = "10px";
                div.style.margin = "10px";

                div.innerHTML = `
                    <h3>${course.title}</h3>
                    <button onclick="openCourse(${course.id})">Открыть</button>
                `;

                container.appendChild(div);
            });

            window.courses = courses;
        } catch (e) {
            console.log("Ошибка загрузки:", e);
        }
    }

    loadCourses();

    // открыть курс
    window.openCourse = function(id) {
        let course = window.courses.find(c => c.id == id);

        document.body.innerHTML = `<h2>${course.title}</h2>
        <button onclick="location.reload()">⬅️ Назад</button>`;

        course.lessons.forEach(l => {
            let div = document.createElement("div");

            div.innerHTML = `
                <iframe width="100%" height="200"
                src="${l.video.replace("watch?v=", "embed/")}"
                frameborder="0"
                allowfullscreen></iframe>
            `;

            document.body.appendChild(div);
        });
    }

    // админ панель
    function openAdmin() {
        document.body.innerHTML = `
            <h2>⚙️ Админ панель</h2>
            <button onclick="addCourse()">➕ Курс</button>
            <button onclick="addLesson()">➕ Урок</button>
            <button onclick="location.reload()">⬅️ Назад</button>
        `;
    }

    // добавить курс
    window.addCourse = async function() {
        let title = prompt("Название курса:");

        if (!title) return;

        await fetch(API + "/add_course", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({title})
        });

        alert("Курс добавлен");
    }

    // добавить урок
    window.addLesson = async function() {
        let course_id = prompt("ID курса:");
        let video = prompt("YouTube ссылка:");

        if (!course_id || !video) return;

        await fetch(API + "/add_lesson", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({course_id, video})
        });

        alert("Урок добавлен");
    }

}
</script>

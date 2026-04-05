/* TELEGRAM INIT */
window.onload = () => {
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    // ⚠️ ПОСТАВЬ СЮДА СВОЙ РЕАЛЬНЫЙ СЕРВЕР
    const API = "https://my-course-app-8w99.onrender.com"; // ← ВАЖНО

    let container = document.getElementById("courses");

    if (!container) {
        container = document.createElement("div");
        container.id = "courses";
        document.body.appendChild(container);
    }

    /* ЗАГРУЗКА КУРСОВ */
    async function loadCourses() {
        try {
            let res = await fetch(API + "/courses");
            let courses = await res.json();

            container.innerHTML = "";

            courses.forEach(course => {
                let div = document.createElement("div");

                div.style.background = "white";
                div.style.padding = "12px";
                div.style.margin = "10px 0";
                div.style.borderRadius = "10px";

                div.innerHTML = `
                    <h3>${course.title}</h3>
                    <button onclick="openCourse(${course.id})">Открыть</button>
                `;

                container.appendChild(div);
            });

            window.courses = courses;

        } catch (e) {
            console.log("Ошибка:", e);
            alert("❌ Сервер не работает");
        }
    }

    loadCourses();

    /* ОТКРЫТЬ КУРС */
    window.openCourse = function(id) {
        let course = window.courses.find(c => c.id == id);

        document.body.innerHTML = `
            <button onclick="location.reload()">⬅ Назад</button>
            <h2>${course.title}</h2>
            <div id="videos"></div>
        `;

        let videos = document.getElementById("videos");

        course.lessons.forEach(l => {
            let videoId = getYouTubeId(l.video);

            let div = document.createElement("div");
            div.style.marginBottom = "15px";

            div.innerHTML = `
                <iframe width="100%" height="220"
                src="https://www.youtube.com/embed/${videoId}"
                frameborder="0"
                allowfullscreen></iframe>
            `;

            videos.appendChild(div);
        });
    };

    /* YOUTUBE ID */
    function getYouTubeId(url) {
        let match = url.match(/(?:v=|youtu\\.be\\/)([^&]+)/);
        return match ? match[1] : url;
    }

    /* АДМИН */
    window.openAdmin = function() {
        document.body.innerHTML = `
            <h2>⚙️ Админ панель</h2>

            <button onclick="addCourse()">➕ Курс</button>
            <button onclick="addLesson()">➕ Урок</button>
            <button onclick="location.reload()">⬅ Назад</button>
        `;
    };

    /* ДОБАВИТЬ КУРС */
    window.addCourse = async function() {
        let title = prompt("Название курса:");
        if (!title) return;

        await fetch(API + "/add_course", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ title })
        });

        alert("✅ Курс добавлен");
    };

    /* ДОБАВИТЬ УРОК */
    window.addLesson = async function() {
        let course_id = prompt("ID курса:");
        let video = prompt("YouTube ссылка:");

        if (!course_id || !video) return;

        await fetch(API + "/add_lesson", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ course_id, video })
        });

        alert("✅ Урок добавлен");
    };
};

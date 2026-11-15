document.addEventListener('DOMContentLoaded', function() {
    const check_sound = document.getElementById("sound_on_off")
    const poster1 = document.getElementById("serparVSninosaur")
    const digimontheme = new Audio(poster1.dataset.audio)
    const input = document.getElementById("image-input")
    const preview = document.getElementById("preview")
    const icon = document.getElementById("upload-icon")
    const ran_atk = document.getElementById("ran_atk")
    const panels = document.querySelectorAll('.nav-collapse')
    const toggle_button = document.querySelector('[data-bs-target=".nav-collapse"]')
    const new_monster = document.getElementById("newMonster")
    const login = document.getElementById("login_li")
    const logout = document.getElementById("logout_li")
    const register = document.getElementById("register_li")
    const user = document.querySelector("#data").innerHTML

    if (localStorage.getItem('navbarOpen') === 'true') {
        panels.forEach(panel => panel.classList.add('show'));
        toggle_button.classList.remove('collapsed');
        toggle_button.setAttribute('aria-expanded', 'true');
    }
    panels.forEach(panel => {
        panel.addEventListener('shown.bs.collapse', () => localStorage.setItem('navbarOpen', 'true'));
        panel.addEventListener('hidden.bs.collapse', () => localStorage.setItem('navbarOpen', 'false'));
    })

    ran_atk.addEventListener('click', () => {
        const new_atk = document.getElementById("new_atk")
        const upload = document.getElementById("upload_btn")
        fetch('newatk',{
            method: 'GET',
        })
        .then (response => {
            if (!response.ok) throw new Error ("Request failed");
            return response.json();
        })
        .then (result => {
            const atk = document.createElement('h2');
            atk.textContent = `${result.attack} damage: ${result.atk}`;
            new_atk.append(atk)
            document.getElementById("attack_input").value = result.attack;
            ran_atk.remove()
            upload.hidden = false;
        })
        .catch(error => console.error(error))
    })

    input.addEventListener('change', () => {
        const file = input.files[0];
        if (!file) return;
        preview.src = URL.createObjectURL(file);
        preview.hidden = false;
        icon.style.display = 'none';
    })

    // replace this with ajax using fetch and all that
    // poster1.addEventListener('mouseover', () => {
    //     if (check_sound.checked == true) {
    //         digimontheme.play();    
    //     }
    // })
    // poster1.addEventListener('mouseleave', () => {
    //     digimontheme.pause();
    //     digimontheme.currentTime = 0;
    // })


})

document.addEventListener('DOMContentLoaded', function() {
    const check_sound = document.getElementById("sound_on_off")
    const poster1 = document.getElementById("serparVSninosaur")
    const digimontheme = new Audio(poster1.dataset.audio)
    const login = document.getElementById("login_li")
    const logout = document.getElementById("logout_li")
    const register = document.getElementById("register_li")
    const user = document.querySelector("#data").innerHTML
    if (user === "Unregistered user detected please login") {
        logout.style.display = 'none'
        login.style.display = 'block'
        register.style.display = 'block'
    } else {
        register.style.display = 'none'
        login.style.display = 'none'
        logout.style.display = 'block'
    };
    poster1.addEventListener('mouseover', () => {
        if (check_sound.checked == true) {
            digimontheme.play();    
        }
    })
    poster1.addEventListener('mouseleave', () => {
        digimontheme.pause();
        digimontheme.currentTime = 0;
    })
})
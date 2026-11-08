document.addEventListener('DOMContentLoaded', function() {
    const check_sound = document.getElementById("sound_on_off")
    const poster1 = document.getElementById("serparVSninosaur")
    const digimontheme = new Audio(poster1.dataset.audio)
    const new_monster = document.getElementById("newMonster")
    const login = document.getElementById("login_li")
    const logout = document.getElementById("logout_li")
    const register = document.getElementById("register_li")
    const user = document.querySelector("#data").innerHTML
    poster1.addEventListener('mouseover', () => {
        if (check_sound.checked == true) {
            digimontheme.play();    
        }
    })
    poster1.addEventListener('mouseleave', () => {
        digimontheme.pause();
        digimontheme.currentTime = 0;
    })
    new_monster.addEventListener('click', () => {
        alert("hello :D")
    })
})
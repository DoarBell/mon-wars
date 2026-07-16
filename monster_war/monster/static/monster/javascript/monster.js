
document.addEventListener('DOMContentLoaded', function() {
    const check_sound = document.getElementById("sound_on_off")
    const poster1 = document.getElementById("serparVSninosaur")
    const digimontheme = new Audio(poster1.dataset.audio)
    check_sound.addEventListener('click', () => {
        // create the user log-in to continue this part
    })
    poster1.addEventListener('mouseover', () => {
        digimontheme.play();
    })
    poster1.addEventListener('mouseleave', () => {
        digimontheme.pause();
        digimontheme.currentTime = 0;
    })
})
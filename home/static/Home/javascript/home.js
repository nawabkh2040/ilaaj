console.log("welcome");
// login page and register page 
const btnLogin = document.querySelector('#btn-1');
const wraper = document.querySelector('.wraper');
let cross = document.querySelector('.off');

btnLogin.addEventListener('click', () => {
   wraper.classList.add('active-popup');
})
cross.addEventListener('click', () => {
   wraper.classList.remove('active-popup');
})

// register page
const btnregister = document.querySelector('#btn-2');
const wraperRes = document.querySelector('.wraper-register');
let close = document.querySelector('.close');


btnregister.addEventListener('click', () => {
   wraperRes.classList.add('active-pop');
})

close.addEventListener('click', () => {
   wraperRes.classList.remove('active-pop');
})

//booking page
const bookNowBtn = document.querySelector("#bookNow");
const wraperBooking = document.querySelector('.wraperBooking');
let off = document.querySelector('.band');

bookNowBtn.addEventListener('click', () => {
   wraperBooking.classList.add('active-pop');
})
off.addEventListener('click', () => {
   wraperBooking.classList.remove('active-pop');
})

//PreLoder
function myfunction() {
   document.getElementById("loading").style.display = "none"
}
let menuicn = document.getElementById("menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
	nav.classList.toggle("navclose");
})

// let options = document.querySelectorAll(".nav-option");
// for (var i = 0; i < options.length - 1; i++) {
// 	options[i].addEventListener("click", function () {
// 		var current = document.getElementsByClassName("active");
// 		current[0].className = current[0].className.replace(" active", "");
// 		this.className += " active";
// 	});
// }


// let dashboard = document.querySelector(".dashboard");
// let profile = document.querySelector(".profile");
// let hospital = document.querySelector(".hospital");

// let dashBtn = document.querySelector(".option1");
// let profileBtn = document.querySelector(".option2");
// let hospiBtn = document.querySelector(".option3");

// dashBtn.addEventListener('click', () => {
// 	dashboard.classList.remove("defaultNone");
// 	profile.classList.add("defaultNone");
// 	hospital.classList.add("defaultNone");
// })

// profileBtn.addEventListener('click', () => {
// 	profile.classList.remove("defaultNone");
// 	dashboard.classList.add("defaultNone");
// 	hospital.classList.add("defaultNone");
// })

// hospiBtn.addEventListener('click', () => {
// 	hospital.classList.remove("defaultNone");
// 	dashboard.classList.add("defaultNone");
// 	profile.classList.add("defaultNone");
// })
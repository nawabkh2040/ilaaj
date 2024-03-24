let menuicnUser = document.getElementById("menuicnUser");
let nav = document.querySelector(".navcontainer");

menuicnUser.addEventListener("click", () => {
	nav.classList.toggle("navclose");
})

let editPen = document.getElementById("editPen");
let saveBtn = document.getElementById("userDetailsSaveBtn");
let userDetails = document.getElementsByClassName("userDetails");

editPen.addEventListener('click', () => {
	saveBtn.classList.toggle("defaultNone");
	userDetails.item(0).classList.toggle("borderOfUserDetails");
	userDetails.item(2).classList.toggle("borderOfUserDetails");
	userDetails.item(0).disabled = false;
	userDetails.item(2).disabled = false;
})

// setting active class

let options = document.querySelectorAll(".nav-option");
for (var i = 0; i < options.length - 1; i++) {
	options[i].addEventListener("click", function () {
		var current = document.getElementsByClassName("active");
		current[0].className = current[0].className.replace(" active", "");
		this.className += " active";
	});
}


let profile = document.querySelector(".profile");
let appointment = document.querySelector(".appointment");
let report = document.querySelector(".report");

let profileBtn = document.querySelector(".option1");
let appointBtn = document.querySelector(".option2");
let reportBtn = document.querySelector(".option3");

appointBtn.addEventListener('click', () => {
	appointment.classList.remove("defaultNone");
	profile.classList.add("defaultNone");
	report.classList.add("defaultNone");
})

profileBtn.addEventListener('click', () => {
	profile.classList.remove("defaultNone");
	appointment.classList.add("defaultNone");
	report.classList.add("defaultNone");
})

reportBtn.addEventListener('click', () => {
	report.classList.remove("defaultNone");
	appointment.classList.add("defaultNone");
	profile.classList.add("defaultNone");
})

console.log("i am responsive js");
let navbar = document.getElementsByClassName('flex');
console.log(navbar);
let ham = document.getElementById( 'ham' );
let clos = document.getElementById( 'cross' );
console.log(ham) ;

ham.addEventListener('click', () =>{
    console.log("click hua");
    navbar.item(0).classList.add("resNav");
    navbar.item(1).classList.add("resNav");
    navbar.item(0).classList.add("blackBg");
    document.getElementById("ham").style.display="none";
    document.getElementById("cross").style.display="block"; 
})
clos.addEventListener('click', () =>{
    console.log("click hua");
    navbar.item(0).classList.remove("resNav");
    navbar.item(1).classList.remove("resNav");
    navbar.item(0).classList.remove("blackBg");
    document.getElementById("ham").style.display="block";
    document.getElementById("cross").style.display="none"; 
})
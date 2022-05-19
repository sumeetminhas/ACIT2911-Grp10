const btnCart = document.querySelector('#cart-logo')
const navContent = document.querySelector('#side-content')
const btnBack = document.querySelector('#back')

navContent.style.display = 'none'

btnCart.addEventListener('click',openSideNav)
btnBack.addEventListener('click',closeSideNav)

function openSideNav(){
    navContent.style.display = 'block'
    btnCart.style.display = "none"
}
function closeSideNav(){
    navContent.style.display = 'none'
    btnCart.style.display = "block"
}


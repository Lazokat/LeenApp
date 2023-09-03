const plain = document.querySelector('.plain')

plain.innerHTML = document.querySelector('.neon').innerHTML

window.onmousemove = (e)=>{
  gsap.to('.follower', {duration:0.3, x:e.x, y:e.y, xPercent:-50, yPercent:-50})
}

const flicker = gsap.timeline()
.to('.neon', {duration:1, opacity:0.7, ease:'elastic.in(2)', yoyo:true, repeat:1})


plain.onmouseout = plain.onmouseover=(e)=>{
  flicker.play(0)
}
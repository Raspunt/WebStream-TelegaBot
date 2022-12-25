



			


document.addEventListener('keydown', (event) => {
  var name = event.key;
  var code = event.code;
  // Alert the key name and key code on keydown
  
  if (name === "ArrowRight"){
    app.SendMotorSignal('R','rightBtn')
  }else if (name === "ArrowDown"){
    app.SendMotorSignal('NAZ','downBtn')
  }else if (name === "ArrowLeft"){
    app.SendMotorSignal('L','leftBtn')
  }else if (name === "ArrowUp"){
    app.SendMotorSignal('V','upBtn')
  }
  
  // console.log(name )

}, false);






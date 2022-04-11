let tries = 0;
spot = 0;
wordToGuess = "party";
function setUpTableRow(){
    spot = 0 ;
    let backDiv = document.getElementById("backDiv")
    let x = 0;
    console.log('gets to while loop')
    while(x < 5){
        let div = document.createElement("div");
        div.style.display = 'inline-block';
        div.style.backgroundColor = 'lightgray';
        div.style.width = '75px';
        div.style.height = '75px';
        div.style.margin = '10px';
        div.style.border = 'none';
        div.style.borderRadius = '5px';
        
        console.log(div.id)
        let input = document.createElement("input")
        input.style.width = '75px';
        input.style.height = '75px';
        input.style.textAlign = 'center';
        input.style.fontSize = '60px';
        input.style.border = 'none';
        input.style.borderRadius = '5px';
        // input.disabled = true;
        
        input.id = x.toString();
        input.maxLength = "1";
        div.appendChild(input);
        backDiv.appendChild(div);
        
        x = x + 1
        document.getElementById("0").focus();
    }

    for(let i = 0; i < 5; i++){
        let id = i.toString()
        let box = document.getElementById(id);
        box.onkeyup = function(){
            moveCursor();
        }
        box.addEventListener("keyup", function(event) {

            if (event.keyCode === 8) {
              // Cancel the default action, if needed
              event.preventDefault();
              // Trigger the button element with a click
              deleteLetter()
            }
          });
    }

}

function deleteLetter(){
    if(spot == 0){

    }
    else{
        spot = spot - 1
        let currentSpot = document.getElementById(spot);
        currentSpot.value = null;
        currentSpot.focus();
    }
}

function moveCursor(){
    x = spot.toString();
    let currentSpot = document.getElementById(x);
    if(currentSpot.value.length == 1){
        console.log("hits move cursor");
        let focusSpot = spot;
        if(spot == 4){
            return
        }
        else{
            focusSpot = spot + 1;
            focusSpot = focusSpot.toString();
            console.log(focusSpot)
            let thing = document.getElementById(focusSpot);
            thing.focus();
        }
        spot = spot + 1;
    }
    if(currentSpot.value.length == 0){
        spot = spot
    }
    
    
}

function check(){
    guess = ""
    for(let i = 0; i < 5; i++){
        let id = i.toString()
        let box = document.getElementById(id);
        guess += box.value
    }
    if(guess.length != 5){
        return
    }
    if(guess.toLowerCase() == wordToGuess){
        for(let i = 0; i < 5; i++){
            let id = i.toString()
            let box = document.getElementById(id);
            box.style.backgroundColor = 'green';
        }
        return
    }
    else{
        

        let x = 0;
        while(x < 5){
            for(let i = 0; i < 5; i++){
                let id = i.toString()
                let box = document.getElementById(id);
                if(i == x && wordToGuess[i] == guess[i]){
                    box.style.backgroundColor = 'green';
                }
                if(i != x && wordToGuess[x] == guess[i]){
                    if(box.style.backgroundColor == 'green'){
                        continue;
                    }
                    else{
                        box.style.backgroundColor = 'yellow';
                    }
                    
                }
            }
            x++;
        }
        
        for(let i = 0; i < 5; i++){
            let id = i.toString()
            let box = document.getElementById(id);
            box.disabled = true;
            box.style.color = 'black';
            box.id = 'none';
        }
        tries = tries + 1;
        if(tries == 6){
            alert('The word was ' + wordToGuess + " you dumb bitch");
            return;
        }
    }
    setUpTableRow()
    document.getElementById("0").focus();
    console.log(guess)
}

function setUp(){

    let backDiv = document.createElement("div");
    backDiv.id = "backDiv";
    backDiv.style.backgroundColor = 'darkgray';
    backDiv.style.width = '480px';
    backDiv.style.height = '600px';
    backDiv.style.margin = 'auto';
    backDiv.style.marginTop = '-25px';
    document.body.appendChild(backDiv);
    setTimeout(5);
    setUpTableRow();
    
}

// setUpTableRow()
setUp();

addEventListener("keyup", function(event) {

    if (event.keyCode === 13) {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      check()
    }
  });
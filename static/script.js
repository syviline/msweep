function sendRequest(data) {
    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest()

        xhr.open("POST", "/")
        xhr.send(JSON.stringify(data))

        xhr.timeout = 2000

        xhr.onload = () => {
            if (xhr.response == "error")
                reject(xhr.response)
            resolve(xhr.response)
        }
        
        xhr.onerror = () => {
            reject(xhr.response)
        }
    })
}

function createElement(name, ...args) {
    let elem = document.createElement(name)
    for (let i of args) {
        elem.classList.add(i)
    }
    return elem
}

function renderField(field) {
    fieldSpan = document.querySelector(".game")
    fieldSpan.innerText = ""
    fieldSpan.style.display = "block"
    for (let i in field) {
        let row = createElement("span", "row", `row-${i}`)
        fieldSpan.appendChild(row)
        for (let j in field[i]) {
            let elem = createElement("span", "col", `elem-${i}`)
            elem.innerText = field[i][j]
            elem.addEventListener('click', () => {
                makeMove(i, j)
            })
            elem.addEventListener('contextmenu', (e) => {
                e.preventDefault()
                makeFlag(i, j)
            })
            row.appendChild(elem)
        }
    }
}

function displayMessage(message, color="#D00") {
    let header = document.querySelector("header")
    header.style.backgroundColor = color
    let header_text = document.querySelector("header .logo")
    header_text.innerText = message
    header_text.style.fontSize = "22px"
}

function doNotDisplayMessage() {
    document.querySelector("header").style.backgroundColor = "#222"
    document.querySelector("header .logo").innerText = "Minesweeper"
    document.querySelector(".stop_game").innerText = "Stop the game"
    document.querySelector(".stop_game").style.display = "none"
    document.querySelector("header .logo").style.fontSize = "50px"
}

function stopGame() {
    document.querySelector(".game").style.display = "none"
    document.querySelector(".ongamestart").style.display = "block"
    doNotDisplayMessage()
}

function makeMove(x, y) {
    req = sendRequest({type: 'move', x: x, y: y})
    req.then(response => {
        console.log(response)
        renderField(JSON.parse(response))
    })
    req = sendRequest({type: 'state'})
    req.then(response => {
        if (response == "fail") {
            displayMessage("Вы проиграли.")
            document.querySelector(".stop_game").innerText = "New Game"
        } else if (response == "won") {
            displayMessage("Вы выиграли!", "#0D0")
            document.querySelector(".stop_game").innerText = "New Game"
        }
    })
}

function makeFlag(x, y) {
    req = sendRequest({type: "flag", x: x, y: y})
    req.then(response => {
        renderField(JSON.parse(response))
    })
}

req = sendRequest({type: "get_field"})
req.then(response => {
    if (response != "100") {
        document.querySelector(".ongamestart").style.display = "none"
        document.querySelector(".stop_game").style.display = "block"
        renderField(JSON.parse(response))
    }
})

let submitButton = document.querySelector(".submit_game")
submitButton.addEventListener('click', () => {
    doNotDisplayMessage()
    let fieldSize = document.querySelector(".field_size").value
    let minesAmount = document.querySelector(".mines_amount").value
    if (minesAmount >= Math.floor((fieldSize * fieldSize) / 2)) {
        displayMessage("Мин на карте при данном размере поля не может быть больше чем " + Math.round((fieldSize * fieldSize) / 2))
        return
    }
    if (fieldSize > 30) {
        displayMessage("Поле не может быть размером больше 30")
        return
    }
    document.querySelector(".stop_game").style.display = "block"
    
    let req = sendRequest({type: "start_game", field_size: fieldSize, mines_amount: minesAmount})
    req.then(response => {
        document.querySelector(".ongamestart").style.display = "none"
        renderField(JSON.parse(response))
    })
})

let stopGameButton = document.querySelector(".stop_game")
stopGameButton.addEventListener('click', () => {
    let req = sendRequest({type: "stop_game"})
    stopGame()
})
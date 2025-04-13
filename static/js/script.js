
function fazerCadastro(event){
    event.preventDefault()

    let novoUsername = document.getElementById("novoUsername").value
    let novaSenha = document.getElementById("novaSenha").value

    fetch("/cadastro", {
        method: "POST", 
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ novoUsername, novaSenha })
    })
    .then(res => res.json())
    .then(data =>{
        console.log("Resposta do servidor", data)
        document.getElementById("resultadoCadastro").innerText = data.mensagem
    })

    .catch(error =>{
        document.getElementById("resultadoCadastro").innerText = "Erro ao se conectar com o servidor"
        document.getElementById("resultadoCadastro").style.color = "red"
        console.error(error)
    })
}

function fazerLogin(event){
    event.preventDefault()

    let username = document.getElementById("username").value
    let password = document.getElementById("password").value

    fetch("/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password }),
        credentials: "include"
    })
    .then(res => res.json())
    .then(data =>{
        console.log("Resposta do servidor", data)
        document.getElementById("resultadoLogin").innerText = data.mensagem
        if(data.mensagem === "Login feito com sucesso"){
            document.getElementById("username").value = ""
            document.getElementById("password").value = ""
            window.location.href = "/chat"
        }
    })
    .catch(error =>{
        document.getElementById("resultadoLogin").innerText = "Erro ao se conectar com o servidor"
        document.getElementById("resultadoLogin").style.color = "red"
        console.error(error)
    })
}
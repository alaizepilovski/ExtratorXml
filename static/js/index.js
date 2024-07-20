const url_origin = document.location.origin
let name_url = document.location.pathname

let importarXml = document.querySelector("#tratarXml")
let xmlFile = document.querySelector("#xml")

if (name_url.includes('importar')){
    importarXml.addEventListener('click', tratarXml)
}

function tratarXml() {
    console.log(xmlFile.files)

    if(xmlFile.files[0]){
        let loading = document.querySelector("#loading")
        loading.style.display = "block"
        ocultarReexibirUpload()
    }
}

function ocultarReexibirUpload(){
    let statusCard = document.querySelector("#cardUpload")

    if(statusCard.style.display === "none"){
        statusCard.style.display = "block"
    } else {
        statusCard.style.display = "none"
    }
}


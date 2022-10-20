const resultSection = document.getElementById("result-section")
const resultText = document.getElementById("result-text")
const resultSubtext = document.getElementById("result-subtext")

const textarea = document.getElementById("text")
const form = document.getElementById("entry-form")

const BASE_URL = form.action

const textValues = {
    "suicide": {
        "result-text": "PROPENSO AL SUICIDIO",
        "result-subtext": "Se determinó que el mensaje demuestra una gran probabilidad de que el usuario esté presentando tendencias suicidas. Se recomienda contactar al usuario para invitarlo a un proceso de recuperación y protección. "
    },
    "nosuicide": {
        "result-text": "NO PROPENSO AL SUICIDIO",
        "result-subtext": "Se determinó que el mensaje no demuestra una gran probabilidad de que el usuario esté presentando tendencias suicidas. No hay necesidad de recomendar acciones drásticas a favor del usuario."
    },
    "default": {
        "result-text": "",
        "result-subtext": "Por favor ingresar y enviar el mensaje que se desea analizar."
    },
    "error": {
        "result-text": "ERROR",
        "result-subtext": "Se presento un error en el modelo, o en el servidor. Por favor leer la consola para investigar."
    },
}

async function submit(e){
    e.preventDefault()
    resultSection.classList.remove("nosuicide", "suicide")
    resultSection.classList.add("loading")
    resultText.innerText = "Cargando..."

    const textContent = textarea.value.trim()
    let result = null
    /*"response": "suicide",
                "original_input": data*/
    try {
        result = (await axios.post(`${BASE_URL}comment/predict`, {text: textContent})).data
        resultSection.classList.remove("nosuicide", "suicide", "loading")
        resultSection.classList.add(result["response"])
        applyText(result["response"])

    } catch (error) {
        applyText("error")
        console.error(error)
    }


}
function applyText(response){
    resultText.innerText = textValues[response]["result-text"]
    resultSubtext.innerText = textValues[response]["result-subtext"]
}

function onTextSelection(){
    resultSection.classList.remove("nosuicide", "suicide", "loading")
    applyText("default")
}

textarea.addEventListener("input", onTextSelection)
form.addEventListener("submit", submit)
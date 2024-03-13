// vanilla aah looking typescript component for dumb mf mapbox popup garbajo
import type Location from "./Location"

export default function Popup(location : Location, onclick: () => void): string {
    const infoSection = InfoSection(location)
    const formSection = FormSection(10, onclick)
    
    const popup = document.createElement('div')
    popup.setAttribute('style', 'display: flex; flex-direction: row;')
    popup.appendChild(infoSection)
    popup.appendChild(formSection)    
    return popup.outerHTML
}

function FormSection(court_count : number, onsubmit: () => void) {
    const form = document.createElement('form')
    form.setAttribute('onsubmit', 'event.preventDefault()')

    // Courts Occupied
    const cLabel = document.createElement('label')
    cLabel.textContent = 'Courts Occupied:'
    cLabel.setAttribute('for', 'courtsOccupied')

    const cInput = document.createElement('input')
    cInput.type = 'number'
    cInput.id = 'courtsOccupied'
    cInput.name = 'courtsOccupied'
    cInput.min = '0'
    cInput.max = String(court_count)
    cInput.required = true

    // Number Waiting
    const nLabel = document.createElement('label')
    nLabel.textContent = 'Number Waiting:'
    nLabel.setAttribute('for', 'numberWaiting')

    const nInput = document.createElement('input')
    nInput.type = 'number'
    nInput.id = 'numberWaiting'
    nInput.name = 'numberWaiting'
    nInput.min = '0'
    nInput.max = String(court_count)
    nInput.required = true

    // Submit Button
    const submitButton = document.createElement('button')
    submitButton.disabled = false
    submitButton.textContent = 'Update Status'
    submitButton.click = onsubmit

    form.appendChild(cLabel)
    form.appendChild(cInput)
    form.appendChild(nLabel)
    form.appendChild(nInput)
    form.appendChild(submitButton)

    return form
}

function InfoSection(location: Location) {
    const info = document.createElement('div')
    info.classList.add('info')

    const h3 = document.createElement('h3')
    h3.textContent = location.name

    const sub = document.createElement('sub')
    sub.textContent = `Courts: ${location.court_count}`

    const p1 = document.createElement('p')
    p1.textContent = `Estimated Courts Occupied: ${location.courts_occupied}`

    const p2 = document.createElement('p')
    p2.textContent = `Estimated Groups Waiting: ${location.number_waiting}`

    const p3 = document.createElement('p')
    p3.textContent = `Estimated Wait Time: ${formatTime(location.estimated_wait_time)}`

    info.appendChild(h3)
    info.appendChild(sub)
    info.appendChild(p1)
    info.appendChild(p2)
    info.appendChild(p3)

    return info
}

function pluralize(word: string, num: number): string {
    if (num != 1) {
        word += "s"
    }
    return word
}

function formatTime(timeNum: number): string {
    let timeNumArr = String(timeNum).split(":")

    let formattedString = ""
    let hours = timeNumArr[0].startsWith("0") ? timeNumArr[0].substring(1) : timeNumArr[0]
    let minutes = timeNumArr[1].startsWith("0") ? timeNumArr[1].substring(1) : timeNumArr[1]

    formattedString += hours + " "
    formattedString += pluralize("Hour", Number(timeNumArr[0])) + " "
    formattedString += minutes + " "
    formattedString += pluralize("Minute", Number(timeNumArr[1]))
    return formattedString
}
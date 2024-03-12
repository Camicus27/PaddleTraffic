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

export default function Popup(name: string, court_count: number, courts_occupied: number, number_waiting: number, estimated_wait_time: number) : string {

    const htmlReturnValue = 
    `
        <div class="info">
            <h3>${name}</h3>
            <sub>Courts: ${court_count}</sub>
            <p>Estimated Courts Occupied: ${courts_occupied}</p>
            <p>Estimated Groups Waiting: ${number_waiting}</p>
            <p>Estimated Wait Time: ${formatTime(estimated_wait_time)}</p>
        </div>
        <form onsubmit="event.preventDefault()">
            <label for="courtsOccupied">Courts Occupied:</label><br>
            <input type="number" id="courtsOccupied" name="courtsOccupied" min="0" :max="currSelection.court_count"
                v-model="locForm.courts_occupied" required><br><br>
            <label for="numberWaiting">Number Waiting:</label><br>
            <input type="number" id="numberWaiting" name="numberWaiting" min="0"
                :max="(locForm.courts_occupied < currSelection.court_count) ? 0 : 10" v-model="locForm.number_waiting"
                required><br><br>
            <button :disabled="submitDataDisabled">
                Update Status
            </button>
        </form>

        <script>

        </script>
    `
    return htmlReturnValue
}
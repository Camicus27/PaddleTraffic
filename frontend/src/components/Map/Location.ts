export default interface Location {
    id: number
    name: string
    latitude: number
    longitude: number
    court_count: number
    courts_occupied: number
    number_waiting: number
    estimated_wait_time: number
}
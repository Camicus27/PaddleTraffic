import { ref } from 'vue'

export const generalTextRule = ref([
    (value: string) => {
        if (value) return true

        return 'Missing value.'
    },
])

export const nameRules = ref([
    (value: string) => {
        if (value) return true

        return 'Missing a name.'
    },
    (value: string) => {
        if (value?.length <= 25) return true

        return 'Name must be less than 25 characters.'
    },
])

export const latRules = ref([
    (value: number) => {
        if (value) return true

        return 'Missing value.'
    },
    (value: number) => {
        if (90 > value && value > -90) return true

        return 'Latitude must be between 90 and -90 degrees'
    },
])

export const longRules = ref([
    (value: number) => {
        if (value) return true

        return 'Missing value.'
    },
    (value: number) => {
        if (180 > value && value > -180) return true

        return 'Longitude must be between 180 and -180 degrees'
    },
])

export const courtRules = ref([
    (value: number) => {
        if (value) return true

        return 'Missing value.'
    },
    (value: number) => {
        if (value > 0) return true

        return 'Court count must be a positive number'
    },
])
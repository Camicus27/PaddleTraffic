import { createRouter, createWebHistory } from 'vue-router'
import AboutView from '../views/AboutView.vue'
import MapView from '../views/MapView.vue'
import EventsView from '../views/EventsView.vue'
import EventFormView from '../views/EventFormView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/map'
        },
        {
            path: '/about',
            name: 'about',
            component: AboutView
        },
        {
            path: '/map',
            name: 'map',
            component: MapView
        },
        {
            path: '/matchmaking',
            name: 'matchmaking',
            component: EventsView
        },
        {
            path: '/matchmaking/create-event',
            name: 'create-event',
            component: EventFormView
        },
        {
            path: '/profile/:username?',
            name: 'profile',
            component: ProfileView
        },
    ]
})

export default router
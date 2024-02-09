import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import MapView from '../views/MapView.vue'
import MatchView from '../views/MatchView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
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
            component: MatchView
        },
        {
            path: '/profile',
            name: 'profile',
            component: ProfileView
        },
    ]
})

export default router
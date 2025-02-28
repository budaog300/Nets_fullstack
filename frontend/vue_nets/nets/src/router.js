import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/Home.vue';
import Veterans from './components/Veterans.vue';
import Clubs from './components/Clubs.vue';
import Sports from './components/Sports.vue';
import Category from './components/Category.vue';
import Login from './components/users/Login.vue';
import Register from './components/users/Register.vue';
import Profile from './components/users/Profile.vue';
import UpdateProfile from './components/users/UpdateProfile.vue';

const routes = [
    { path: '/', component: Home, name: 'home' },
    { path: '/veterans', component: Veterans, name: 'veterans' },
    { path: '/clubs', component: Clubs, name: 'clubs' },   
    { path: '/sports', component: Sports, name: 'sports' },  
    { path: '/category', component: Category, name: 'category' },
    { path: '/login', component: Login, name: 'login' }, 
    { path: '/register', component: Register, name: 'register' }, 
    { path: '/profile', component: Profile, name: 'profile' }, 
    { path: '/update-profile', component: UpdateProfile, name: 'updateprofile' },   
];

const router = createRouter({
    routes,
    history: createWebHistory()  
});

export default router;

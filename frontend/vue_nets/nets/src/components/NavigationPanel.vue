<template>
    <div class="auth-container">
        <template v-if="isAuthenticated">
            <router-link class="nav-button" :to="{ name: 'profile' }" v-if="user">{{ user.username }}</router-link>
            <button class="nav-button" @click="handleLogout">Выход</button>
        </template>
        <template v-else>
            <router-link class="nav-button" :to="{ name: 'login' }"> <i class="fa fa-sign-in" aria-hidden="true"></i> Войти</router-link>
            <router-link class="nav-button" :to="{ name: 'register' }"> <i class="fa fa-user-plus" aria-hidden="true"></i> Зарегистрироваться</router-link>
        </template>
    </div>
    <div class="button-container">
        <router-link class="nav-button" :to="{ name: 'home' }">Главная</router-link>
        <router-link class="nav-button" :to="{ name: 'sports' }">Виды спорта</router-link>
        <router-link class="nav-button" :to="{ name: 'category' }">Категории</router-link>
        <router-link class="nav-button" :to="{ name: 'clubs' }">Клубы</router-link>
        <router-link class="nav-button" :to="{ name: 'veterans' }">Ветераны спорта</router-link>    
        
    </div>
</template>

<script>
import { getUserProfile, logoutUser } from '../services/userService';

export default {
    data() {
        return {
            user: null 
        }
    },
    computed: {
        isAuthenticated() {
            return localStorage.getItem('accessToken') !== null; 
        }
    },
    async created() {
        if (this.isAuthenticated) {
            try {
                this.user = await getUserProfile();
            } catch (error) {
                console.error('Ошибка получения данных пользователя:', error);
                this.$router.push({ name: "login" });
            }
        }
    },
    methods: {
        async handleLogout () {
            try {
                await logoutUser();
                this.$router.push({ name: "login" });
            } 
            catch (error) {
                console.error('Ошибка при выходе:', error);
            }
        }
       
    }

}
</script>

<style scoped>

</style>

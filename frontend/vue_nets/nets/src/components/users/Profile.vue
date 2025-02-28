<template>
    <NavigationPanel />    
    <div class="profile-container">
        <h2>Профиль</h2>
        <div v-if="user">
            <img :src="`http://localhost:8000${user.photo}`" alt="Аватарка" class="avatar" v-if="user.photo" />
            <div class="user-info">
                <p><strong>Фамилия:</strong> {{ user.last_name }}</p>
                <p><strong>Имя:</strong> {{ user.first_name }}</p>
                <p><strong>Дата рождения:</strong> {{ formatDate(user.date_birth) }}</p>
                <p><strong>Email:</strong> {{ user.email }}</p>          
                <p><strong>Логин:</strong> {{ user.username }}</p>  
            </div> 
            <router-link class="nav-button" :to="{ name: 'updateprofile' }" v-if="user">Редактировать профиль</router-link> 
        </div>
        <div v-else>
            <p>Загрузка данных...</p>
        </div>
    </div>

</template>

<script>
import NavigationPanel from '../NavigationPanel.vue';
import { getUserProfile } from '../../services/userService';
export default {  
    name: 'Profile', 
    components: {
        NavigationPanel
    },
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
        
        formatDate(dateString) {
            if (!dateString) return 'Не указано';
            const date = new Date(dateString);
            return date.toLocaleDateString('ru-RU', {
                year: '2-digit',
                month: '2-digit',
                day: 'numeric',
            });
        } 
    },
}

</script>
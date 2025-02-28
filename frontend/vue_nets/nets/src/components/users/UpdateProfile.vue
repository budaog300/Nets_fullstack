<template>
    <template v-if="isAuthenticated">
        <router-link class="nav-button" :to="{ name: 'profile' }" v-if="user">Вернуться к профилю</router-link>
        <div class="register-container">
            <h2>Редактировать профиль</h2>
            <form id="profile-form" @submit.prevent="updateProfile">
                <input type="text" v-model="first_name" placeholder="Имя"/>
                <input type="text" v-model="last_name" placeholder="Фамилия"/>  
                <input type="date" v-model="date_birth"/>
                <input type="text" v-model="username" placeholder="Логин"/>
                <input type="email" v-model="email" placeholder="Электронная почта"/>
                <input type="password" v-model="password" placeholder="Пароль"/>
                <input type="file" @change="onFileChange"/>

                <button type="submit">Сохранить изменения</button>
            </form>    
            
        </div>
    </template>
</template>

<script>
import { getUserProfile, updateUserProfile } from '../../services/userService';
export default {    
    components: {       
          
    },  
    data() {
        return { 
            user: null,
            first_name: '',
            last_name: '',
            date_birth: '',
            username: '',
            email: '',
            password: '',
            file: '',
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
                this.first_name = this.user.first_name;
                this.last_name = this.user.last_name;
                this.date_birth = this.user.date_birth;
                this.username = this.user.username;
                this.email = this.user.email;
            } catch (error) {
                console.error('Ошибка получения данных пользователя:', error);
                this.$router.push({ name: "login" });
            }
        }
    },
    methods: { 
        async updateProfile() {
            const formData = new FormData();
            formData.append('first_name', this.first_name);
            formData.append('last_name', this.last_name);            
            formData.append('username', this.username);
            formData.append('email', this.email);
            if (this.date_birth) {
                formData.append('date_birth', this.date_birth);
            }
            if (this.password) {
                formData.append('password', this.password);
            }       
            if (this.file) {
                formData.append('photo', this.file);
            }
            try {
                await updateUserProfile(formData)
                this.user = await getUserProfile();
                this.$router.push({ name: "profile" });
                console.log('Данные обновлены успешно!')
            }
            catch (error) {
                console.error('Ошибка обновления профиля:', error);
            }
        },
        
        onFileChange(event) {
            const file = event.target.files[0];
            console.log(file)
            if (file) {
                this.file = file;         
            }
        },
    },

}

</script>
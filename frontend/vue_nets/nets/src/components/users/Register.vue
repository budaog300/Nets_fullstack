<template>
  <router-link class="home-button" :to="{ name: 'home' }">Главная</router-link>
  <div class="register-container">
    <h2>Регистрация</h2>
    <form id="register-form" @submit.prevent="registerUser">
      <input type="text" v-model="username" placeholder="Имя пользователя" required />
      <input type="email" v-model="email" placeholder="Электронная почта" required />
      <input type="password" v-model="password" placeholder="Пароль" required />
      <button type="submit">Зарегистрироваться</button>
    </form>    
    <p>{{ error }}</p> 
    <p>Уже есть аккаунт?<router-link class="auth-link" :to="{ name: 'login' }"> Войти</router-link></p>
  </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        url: ``,  
        username: '',
        email: '',
        password: '',
        error: '',
      };
    },
    methods: {
      async registerUser() {    
        this.url = "http://localhost:8000/users/api/v1/register/"                 
        try {
          const response = await this.$axios.post(this.url, {
            username: this.username,
            email: this.email,
            password: this.password
          });

          localStorage.setItem('accessToken', response.data.access);
          localStorage.setItem('refreshToken', response.data.refresh);
          console.log("Регистрация успешна:", response.data); 
          this.$router.push({ name: "profile" });   
                    
        }
        catch (error) {
          console.error('Ошибка регистарции пользователя:', error);
          this.error = "Ошибка регистарции пользователя."    
        } 
        
      },
    },
  };
  </script>
  
  <style scoped>
  
  </style>
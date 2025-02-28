<template>
  <router-link class="home-button" :to="{ name: 'home' }">Главная</router-link>
  <div class="register-container">
    <h2>Авторизация</h2>
    <form id="register-form" @submit.prevent="loginUser">
      <input type="text" v-model="username" placeholder="Имя пользователя" required />
      <input type="password" v-model="password" placeholder="Пароль" required />
      <button type="submit">Войти</button>
    </form>
    <p>{{ error }}</p>
    <p>Нет аккаунта? <router-link class="register-link" :to="{ name: 'register' }"
      >Зарегистрироваться</router-link>
    </p>
  </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        url: ``,
        username: '',
        password: '',
        error: '',
      }
    },
    methods: {
      async loginUser() {
        this.url = "http://localhost:8000/users/api/v1/login/"  
        try {
          console.log("Отправляемые данные:", { username: this.username, password: this.password });
          const response = await this.$axios.post(this.url, {
            username: this.username,           
            password: this.password
        })
        
        localStorage.setItem('accessToken', response.data.access);
        localStorage.setItem('refreshToken', response.data.refresh);
        console.log("Авторизация успешна:", response.data);  
        this.$router.push({ name: "profile" });
       
        } 
        catch (error) {
          if (error.response && error.response.status === 401) {
            console.error("Неверные данные для входа:", error.response.data.error);
            this.error = "Неверное имя пользователя или пароль."          
          } else {
            console.error("Ошибка авторизации:", error.message);
             this.error = "Произошла ошибка при авторизации."          
          }
        }
       
      },
    },
  };
  </script>
  
  <style scoped>
  
  </style>
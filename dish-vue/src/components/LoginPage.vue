<template>
    <div>
        <h1>Login Page</h1>
        <input type="text" v-model="username" placeholder="Username">
        <input type="password" v-model="password" placeholder="Password">
        <button @click="login">Login</button>
        <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            username: '',
            password: '',
            errorMessage: ''
        };
    },
    methods: {
        async login() {
            try {
                const response = await axios.post('http://127.0.0.1:8000/login', {
                    account: this.username,
                    password: this.password
                });
                if (response.status === 200) {
                    const data = response.data;
                    this.$router.push({ name: 'BabyPage', params: { userId: data.user_id } });
                } else {
                    const errorData = response.data;
                    this.errorMessage = errorData.detail;
                }
            } catch (error) {
                console.error('Error logging in:', error);
                this.errorMessage = 'An error occurred while logging in. Please try again.';
            }
        }

    }
};
</script>

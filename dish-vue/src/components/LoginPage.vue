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
                const response = await fetch('http://127.0.0.1:8000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        account: this.username,
                        password: this.password
                    })
                });
                if (response.ok) {
                    const data = await response.json();
                    this.$router.push({ name: 'UserProfile', params: { userId: data.user_id } });
                } else {
                    // 登录失败，显示错误信息
                    const errorData = await response.json();
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
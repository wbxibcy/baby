<template>
  <div class="background"></div>
  <el-form class="login-box">
    <el-form-item>
      <el-text class="mx-1">欢迎来到宝宝辅食！</el-text>
    </el-form-item>
    <el-form-item>
      <el-input placeholder="用户名" v-model="username"></el-input>
    </el-form-item>
    <el-form-item>
      <el-input placeholder="密码" type="password" v-model="password"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="login" round>登录</el-button>
    </el-form-item>
  </el-form>
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

<style scoped>
* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  font-family: Arial, sans-serif;
}

#app {
  height: 100%;
  width: 100%;
}

.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.01), rgba(255, 255, 255, 0.5)), url('../assets/login.jpg') no-repeat center center;
  background-size: cover;
  z-index: -1;
}

.login-box {
  width: 300px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  text-align: center;
  position: absolute;
  top: 50%;
  right: 10%; /* 将 right 设置为 0 */
  transform: translate(0, -50%); /* 使用 translate 函数来垂直居中 */
  display: flex; /* 使用 flex 布局 */
  flex-direction: column; /* 垂直排列子元素 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
</style>

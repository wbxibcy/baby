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
  <el-dialog :model-value="showDialog" title="错误提示" @close="showDialog = false">
    <p>{{ errorMessage }}</p>
    <template #footer>
      <el-button @click="showDialog = false">确定</el-button>
    </template>
  </el-dialog>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      showDialog: false
    };
  },
  methods: {
    validateInput() {
      const usernameRegex = /^[a-zA-Z0-9_]{3,}$/; // 允许字母、数字和下划线，至少3个字符
      if (!this.username) {
        this.errorMessage = '账号不能为空';
        this.showDialog = true;
        return false;
      } else if (!usernameRegex.test(this.username)) {
        this.errorMessage = '账号格式不正确，至少3个字符，只能包含字母、数字和下划线';
        this.showDialog = true;
        return false;
      }

      if (!this.password) {
        this.errorMessage = '密码不能为空';
        this.showDialog = true;
        return false;
      } else if (this.password.length < 3) {
        this.errorMessage = '密码长度不能少于3位';
        this.showDialog = true;
        return false;
      }

      return true;
    },
    async login() {
      if (!this.validateInput()) {
        return;
      }

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
          this.showDialog = true;
        }
      } catch (error) {
        console.error('Error logging in:', error);
        this.errorMessage = '账号或者密码错误，请重新输入';
        this.showDialog = true;
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
  right: 50%; /* 将 right 设置为 50% */
  transform: translate(50%, -50%); /* 使用 translate 函数来垂直居中 */
  display: flex; /* 使用 flex 布局 */
  flex-direction: column; /* 垂直排列子元素 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
</style>

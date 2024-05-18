<template>
  <div class="personal-page">
    <h2>个人主页</h2>
    <el-card v-if="user" class="user-card">
      <p><strong>姓名:</strong> {{ user.name }}</p>
      <p><strong>昵称:</strong> {{ user.nickname }}</p>
      <p><strong>性别:</strong> {{ user.gender }}</p>
      <p><strong>账号:</strong> {{ user.account }}</p>
      <p><strong>电话:</strong> {{ user.phone }}</p>
      <div v-if="user.avatar">
        <p><strong>头像:</strong></p>
        <el-image :src="user.avatar" alt="Avatar" class="avatar"></el-image>
      </div>
    </el-card>
    <el-card v-else class="loading-card">
      <p>加载中...</p>
    </el-card>
  </div>
</template>


<style>
html, body {
  height: 100%;
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

.personal-page {
  background: url('../assets/personal-background.png') no-repeat center center fixed;
  background-size: cover;
  height: 100%; /* Ensures the container takes the full height of the viewport */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

h2 {
  color: #fff;
}

.user-card, .loading-card {
  background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent card background */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  margin: 20px;
}

.avatar {
  max-width: 100px;
  border-radius: 50%;
  margin-top: 10px;
}
</style>




<script>
import { fetchUserProfile } from '../services/api';
import { ElCard, ElImage } from 'element-plus';

export default {
  components: {
    ElCard,
    ElImage
  },
  data() {
    return {
      userId: null,
      user: null,
    };
  },
  created() {
    this.userId = this.$route.params.userId;
    this.getUserProfile();
  },
  methods: {
    async getUserProfile() {
      this.user = await fetchUserProfile(this.userId);
    },
  },
};
</script>

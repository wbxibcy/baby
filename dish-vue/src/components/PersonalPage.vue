<template>
    <div class="personal-page">
      <h2>个人主页</h2>
      <div v-if="user">
        <p><strong>姓名:</strong> {{ user.name }}</p>
        <p><strong>昵称:</strong> {{ user.nickname }}</p>
        <p><strong>性别:</strong> {{ user.gender }}</p>
        <p><strong>账号:</strong> {{ user.account }}</p>
        <p><strong>电话:</strong> {{ user.phone }}</p>
        <div v-if="user.avatar">
          <p><strong>头像:</strong></p>
          <img :src="user.avatar" alt="Avatar" class="avatar">
        </div>
      </div>
      <div v-else>
        <p>加载中...</p>
      </div>
    </div>
  </template>
  
  <script>
  import { fetchUserProfile } from '../services/api';
  
  export default {
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
  
  <style>
  .personal-page {
    background-color: #D4E3B5;
    padding: 20px;
    border-radius: 10px;
    max-width: 600px;
    margin: auto;
  }
  
  .avatar {
    max-width: 100px;
    border-radius: 50%;
    margin-top: 10px;
  }
  </style>
  
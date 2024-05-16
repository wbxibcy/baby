<template>
    <div class="personal-page">
      <h2>个人主页</h2>
      <p>Address specific concerns while incorporating mindfulness practices for improved well-being.</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        userId: null,
      };
    },
    created() {
      this.userId = this.$route.params.userId;
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
  </style>
  
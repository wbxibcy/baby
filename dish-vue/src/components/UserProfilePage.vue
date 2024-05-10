<template>
    <div>
      <h1>User Profile Page</h1>
      <p>User ID: {{ userId }}</p>
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
      // Retrieve user ID from route params
      this.userId = this.$route.params.userId;
    },
  };
  </script>
  
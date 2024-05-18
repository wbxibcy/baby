<template>
  <div class="container">
    <div class="header">
      <div class="title">欢迎使用宝宝辅食管理系统</div>
      <div class="avatar" @click="navigateToPersonalPage">
        <img src="../assets/logo.png" alt="User Avatar" />
      </div>
    </div>
    <div class="intro">
      <h2>纯介绍</h2>
      <p>Daily chaos got you down? Mindfulness helps navigate with focus, clarity, and inner peace. Find your calm center within.</p>
    </div>
    <div class="add-dish" @click="navigateToAddDishPage">
      <h2>增加宝宝辅食</h2>
    </div>
    <div class="history-dish" @click="navigateToHistoryDishPage">
      <h2>历史宝宝辅食</h2>
    </div>
    <div class="personal-page" @click="navigateToPersonalPage">
      <h2>个人主页</h2>
    </div>
  </div>
</template>

<style>
html, body {
  height: 100%;
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

.container {
  display: grid;
  grid-template-areas: 
    "header header header"
    "intro intro intro"
    "add-dish history-dish personal-page";
  gap: 20px;
  padding: 20px;
}

.header {
  grid-area: header;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 10px 20px;
  border-bottom: 1px solid #ddd;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.avatar {
  cursor: pointer;
}

.avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.intro {
  grid-area: intro;
  background: url('../assets/welcome-background.png') no-repeat center center;
  background-size: cover;
  padding: 20px;
  text-align: center;
  color: white; /* Ensure text is visible on background */
}

.add-dish {
  grid-area: add-dish;
  background: url('../assets/addpage-background.png') no-repeat center center;
  background-size: cover;
  padding: 20px;
  cursor: pointer;
  text-align: center;
  color: white; /* Ensure text is visible on background */
}

.history-dish {
  grid-area: history-dish;
  background: url('../assets/history-background.png') no-repeat center center;
  background-size: cover;
  padding: 20px;
  cursor: pointer;
  text-align: center;
  color: white; /* Ensure text is visible on background */
}

.personal-page {
  grid-area: personal-page;
  background: url('../assets/personal-background.png') no-repeat center center;
  background-size: cover;
  padding: 20px;
  cursor: pointer;
  text-align: center;
  color: white; /* Ensure text is visible on background */
}

h2 {
  margin: 0;
}
</style>



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
  methods: {
    navigateToAddDishPage() {
      this.$router.push({ name: 'AddDishPage', params: { userId: this.userId } });
    },
    navigateToHistoryDishPage() {
      this.$router.push({ name: 'HistoryDishPage', params: { userId: this.userId } });
    },
    navigateToPersonalPage() {
      this.$router.push({ name: 'PersonalPage', params: { userId: this.userId } });
    }
  },
};
</script>

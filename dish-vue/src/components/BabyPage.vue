<template>
  <div class="container">
    <div class="header">
      <div class="title">欢迎使用宝宝辅食管理系统</div>
      <div class="avatar" @click="navigateToPersonalPage">
        <img src="../assets/logo.png" alt="User Avatar" />
      </div>
    </div>
    <div class="intro">
      <div class="intro-overlay">
        <h2>是否在为宝宝的辅食选择和管理而烦恼？</h2>
        <p>我们的宝宝辅食管理系统可以帮助你做出更好的决策，确保宝宝获得健康营养的饮食。找到适合宝宝的辅食搭配，让宝宝健康成长。</p>
      </div>
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
html,
body {
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
  padding: 40px 20px;
  text-align: center;
  height: 50vh;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* .intro-overlay {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 20px;
  border-radius: 10px;
} */

.intro h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.intro p {
  font-size: 18px;
  line-height: 1.5;
  color: #191818;
}

.add-dish,
.history-dish,
.personal-page {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  text-align: center;
  color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.add-dish {
  grid-area: add-dish;
  background: url('../assets/addpage-background.png') no-repeat center center;
  background-size: cover;
  height: 20vh;
  width: 40vh;
}

.history-dish {
  grid-area: history-dish;
  background: url('../assets/history-background.png') no-repeat center center;
  background-size: cover;
  height: 20vh;
  width: 50vh;
}

.personal-page {
  grid-area: personal-page;
  background: url('../assets/personal-background.png') no-repeat center center;
  background-size: cover;
  height: 20vh;
  width: 40vh;
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

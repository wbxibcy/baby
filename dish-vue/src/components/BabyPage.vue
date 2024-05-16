<template>
  <div class="container">
    <div class="intro">
      <h2>纯介绍</h2>
      <p>Daily chaos got you down? Mindfulness helps navigate with focus, clarity, and inner peace. Find your calm center within.</p>
    </div>
    <div class="add-dish">
      <h2>增加宝宝辅食</h2>
      <button @click="navigateToAddDishPage">Go to Add Dish Page</button>
    </div>
    <div class="history-dish">
      <h2>历史宝宝辅食</h2>
      <button @click="navigateToHistoryDishPage">Go to History Dish Page</button>
    </div>
    <div class="personal-page">
      <h2>个人主页</h2>
      <button @click="navigateToPersonalPage">Go to Personal Page</button>
    </div>
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

<style>
.container {
  display: grid;
  grid-template-areas: 
    "intro intro intro"
    "add-dish history-dish personal-page";
  gap: 20px;
}

.intro {
  grid-area: intro;
  background-color: #D9BCE3;
  padding: 20px;
  text-align: center;
}

.add-dish {
  grid-area: add-dish;
  background-color: #B5D8CF;
  padding: 20px;
}

.history-dish {
  grid-area: history-dish;
  background-color: #9FD4E5;
  padding: 20px;
}

.personal-page {
  grid-area: personal-page;
  background-color: #D4E3B5;
  padding: 20px;
}
</style>

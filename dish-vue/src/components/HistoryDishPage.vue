<template>
    <div class="history-dish-page">
      <h2>历史宝宝辅食</h2>
      <ul>
        <li v-for="dish in dishes" :key="dish.id">
          <span>{{ dish.name }}</span>
          <img v-if="dish.image" :src="'data:image/jpeg;base64,' + dish.image" alt="Dish Image" style="max-width: 100px;">
          <button @click="deleteDish(dish.id)">Delete</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { fetchDishes, deleteDish } from '../services/api';
  
  export default {
    data() {
      return {
        userId: null,
        dishes: [],
      };
    },
    created() {
      this.userId = this.$route.params.userId;
      this.fetchUserDishes();
    },
    methods: {
      async fetchUserDishes() {
        this.dishes = await fetchDishes(this.userId);
      },
      async deleteDish(dishId) {
        await deleteDish(this.userId, dishId);
        this.fetchUserDishes();
      },
    },
  };
  </script>
  
  <style>
  .history-dish-page {
    background-color: #9FD4E5;
    padding: 20px;
    border-radius: 10px;
    max-width: 600px;
    margin: auto;
  }
  
  .history-dish-page ul {
    list-style: none;
    padding: 0;
  }
  
  .history-dish-page li {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .history-dish-page img {
    margin-left: 10px;
    margin-right: 10px;
  }
  </style>
  
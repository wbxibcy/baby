<template>
    <div class="history-dish-page">
      <h2>历史宝宝辅食</h2>
      <ul>
        <li v-for="dish in dishes" :key="dish.id">
          <span @click="viewIngredients(dish.id)">{{ dish.name }}</span>
          <img v-if="dish.image" :src="'data:image/jpeg;base64,' + dish.image" alt="Dish Image" style="max-width: 100px;" @click="viewIngredients(dish.id)">
          <button @click="deleteDish(dish.id)">Delete</button>
        </li>
      </ul>
  
      <!-- 模态对话框显示食材信息 -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <h3>食材信息</h3>
          <ul>
            <li v-for="ingredient in ingredients" :key="ingredient.name">
              <span>{{ ingredient.name }}: {{ ingredient.quantity }} {{ ingredient.unit }}</span>
            </li>
          </ul>
          <button @click="closeModal">关闭</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { fetchDishes, deleteDish, fetchIngredients } from '../services/api';
  
  export default {
    data() {
      return {
        userId: null,
        dishes: [],
        showModal: false,
        ingredients: [],
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
        await deleteDish(dishId);
        this.fetchUserDishes();
      },
      async viewIngredients(dishId) {
        this.ingredients = await fetchIngredients(this.userId, dishId);
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
      }
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
    cursor: pointer;
  }
  
  .history-dish-page span {
    cursor: pointer;
  }
  
  /* 模态对话框样式 */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
  }
  
  .modal-content h3 {
    margin-top: 0;
  }
  
  .modal-content ul {
    list-style: none;
    padding: 0;
  }
  
  .modal-content li {
    margin-bottom: 10px;
  }
  
  .modal-content button {
    margin-top: 10px;
  }
  </style>
  
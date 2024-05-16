<template>
    <div class="add-dish-page">
      <h2>增加宝宝辅食</h2>
  
      <div v-if="step === 1">
        <form @submit.prevent="nextStep">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="name" placeholder="Dish Name" required>
  
          <label for="image">Image:</label>
          <input type="file" id="image" @change="onFileChange" required>
  
          <label for="favourite">Favourite:</label>
          <input type="checkbox" id="favourite" v-model="favourite">
  
          <button type="submit">Next Step</button>
        </form>
      </div>
  
      <div v-if="step === 2">
        <h3>添加食材</h3>
        <form @submit.prevent="submitIngredients">
          <div v-for="(ingredient, index) in ingredients" :key="index" class="ingredient">
            <label for="ingredient-name">Name:</label>
            <input type="text" v-model="ingredient.name" placeholder="Ingredient Name" required>
  
            <label for="quantity">Quantity:</label>
            <input type="number" v-model="ingredient.quantity" placeholder="Quantity" required>
  
            <label for="unit">Unit:</label>
            <input type="text" v-model="ingredient.unit" placeholder="Unit" required>
  
            <button type="button" @click="removeIngredient(index)">Remove</button>
          </div>
          <button type="button" @click="addNewIngredient">Add Another Ingredient</button>
          <button type="submit">Submit Ingredients</button>
          <button type="button" @click="skipIngredients">Skip Ingredients</button>
        </form>
      </div>
  
      <!-- 模态对话框 -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <h3>{{ modalTitle }}</h3>
          <p>{{ modalMessage }}</p>
          <button @click="stayOnPage">留在这个页面</button>
          <button @click="goToHomePage">返回主页</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { addDish, addIngredients, getDishIdByName } from '../services/api';
  
  export default {
    data() {
      return {
        userId: null,
        name: '',
        image: null,
        favourite: false,
        step: 1,
        showModal: false,
        dishId: null,
        ingredients: [
          { name: '', quantity: '', unit: '' }
        ],
        modalTitle: '',
        modalMessage: '',
      };
    },
    created() {
      this.userId = this.$route.params.userId;
    },
    methods: {
      async nextStep() {
        try {
          const response = await addDish(this.name, this.image, this.favourite, this.userId);
          if (response) { // 确保成功添加菜品
            console.log(this.userId, this.name)
            const dishId = await getDishIdByName(this.userId, this.name);
            if (dishId) {
              this.dishId = dishId; // 获取添加的菜品的ID
              this.step = 2;
            } else {
              this.modalTitle = '错误';
              this.modalMessage = '获取菜品ID失败，请重试。';
              this.showModal = true;
            }
          } else {
            this.modalTitle = '错误';
            this.modalMessage = '添加菜品失败，请重试。';
            this.showModal = true;
          }
        } catch (error) {
          console.error('Error adding dish:', error);
          this.modalTitle = '错误';
          this.modalMessage = '添加菜品时发生错误，请重试。';
          this.showModal = true;
        }
      },
      onFileChange(event) {
        this.image = event.target.files[0];
      },
      addNewIngredient() {
        this.ingredients.push({ name: '', quantity: '', unit: '' });
      },
      removeIngredient(index) {
        this.ingredients.splice(index, 1);
      },
      async submitIngredients() {
        try {
          const payload = {
            uid: this.userId,
            did: this.dishId,
            ingredients: this.ingredients.map(ingredient => ({
              ...ingredient,
              quantity: Number(ingredient.quantity) // 确保数量是数字类型
            }))
          };
          console.log('Submitting ingredients:', payload); // Debug log
          const response = await addIngredients(payload);
          if (response) {
            this.modalTitle = '恭喜你添加成功!';
            this.modalMessage = '你想留在这个页面还是返回主页?';
          } else {
            this.modalTitle = '错误';
            this.modalMessage = '添加食材失败，请重试。';
          }
        } catch (error) {
          console.error('Error adding ingredients:', error);
          this.modalTitle = '错误';
          this.modalMessage = '添加食材时发生错误，请重试。';
        }
        this.showModal = true; // 显示模态对话框
      },
      skipIngredients() {
        this.modalTitle = '恭喜你添加成功!';
        this.modalMessage = '你想留在这个页面还是返回主页?';
        this.showModal = true; // 显示模态对话框
      },
      stayOnPage() {
        this.showModal = false; // 隐藏模态对话框
      },
      goToHomePage() {
        this.$router.push({ name: 'BabyPage', params: { userId: this.userId } });
      }
    },
  };
  </script>
  
  <style>
  .add-dish-page {
    background-color: #B5D8CF;
    padding: 20px;
    border-radius: 10px;
    max-width: 600px;
    margin: auto;
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
  
  .modal-content button {
    margin: 10px;
  }
  
  .ingredient {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
  }
  
  .ingredient button {
    align-self: flex-start;
    margin-top: 5px;
  }
  </style>
  
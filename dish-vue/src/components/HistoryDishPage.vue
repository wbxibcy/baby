<template>
  <div class="history-dish-page">
    <h2>历史宝宝辅食</h2>

    <label for="filter">显示:</label>
    <select id="filter" v-model="filter" @change="applyFilter">
      <option value="all">全部</option>
      <option value="favourite">收藏</option>
    </select>

    <label for="search">搜索:</label>
    <input id="search" v-model="searchQuery" placeholder="搜索菜品..." />
    <button @click="searchDishes">搜索</button>

    <ul>
      <li v-for="dish in filteredDishes" :key="dish.id">
        <span>{{ dish.name }}</span>
        <img v-if="dish.image" :src="'data:image/jpeg;base64,' + dish.image" alt="Dish Image" style="max-width: 100px;" @click="viewIngredients(dish)">
        <button @click="deleteDish(dish.id)">删除</button>
        <button @click="editDish(dish)">编辑</button>
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
        <button @click="openAddIngredientsModal">继续添加食材</button>
      </div>
    </div>

    <!-- 编辑菜品模态对话框 -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h3>编辑菜品</h3>
        <label for="editName">名字:</label>
        <input id="editName" v-model="editDishData.name" />
        <label for="editImage">图片:</label>
        <input id="editImage" type="file" @change="handleImageChange" />
        <button @click="updateDish">更新</button>
        <button @click="closeEditModal">关闭</button>
      </div>
    </div>

    <!-- 添加食材模态对话框 -->
    <div v-if="showAddIngredientsModal" class="modal">
      <div class="modal-content">
        <h3>添加食材</h3>
        <div v-for="(ingredient, index) in newIngredients" :key="index">
          <label for="ingredientName">食材名字:</label>
          <input id="ingredientName" v-model="ingredient.name" />
          <label for="ingredientQuantity">数量:</label>
          <input id="ingredientQuantity" v-model="ingredient.quantity" type="number" />
          <label for="ingredientUnit">单位:</label>
          <input id="ingredientUnit" v-model="ingredient.unit" />
        </div>
        <button @click="addIngredientField">添加更多食材</button>
        <button @click="submitNewIngredients">提交</button>
        <button @click="closeAddIngredientsModal">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
import {
  fetchDishes,
  deleteDish,
  fetchIngredients,
  fetchFavouriteDishes,
  searchDishes,
  updateDish,
  addIngredients
} from '../services/api';

export default {
  data() {
    return {
      userId: null,
      dishes: [],
      favouriteDishes: [],
      searchResults: [],
      filter: 'all',
      searchQuery: '',
      showModal: false,
      showEditModal: false,
      showAddIngredientsModal: false,
      ingredients: [],
      currentDishId: null,
      editDishData: {
        id: null,
        name: '',
        image: null
      },
      newIngredients: [
        { name: '', quantity: '', unit: '' }
      ]
    };
  },
  computed: {
    filteredDishes() {
      if (this.searchQuery) {
        return this.searchResults;
      } else if (this.filter === 'favourite') {
        return this.favouriteDishes;
      }
      return this.dishes;
    }
  },
  created() {
    this.userId = this.$route.params.userId;
    this.fetchUserDishes();
    this.fetchFavouriteDishes();
  },
  methods: {
    async fetchUserDishes() {
      this.dishes = await fetchDishes(this.userId);
    },
    async fetchFavouriteDishes() {
      this.favouriteDishes = await fetchFavouriteDishes(this.userId);
    },
    async deleteDish(dishId) {
      await deleteDish(dishId);
      this.fetchUserDishes();
      this.fetchFavouriteDishes();
    },
    async viewIngredients(dish) {
      this.currentDishId = dish.id;
      this.ingredients = await fetchIngredients(this.userId, dish.id);
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async searchDishes() {
      if (this.searchQuery) {
        this.searchResults = await searchDishes(this.userId, this.searchQuery);
      } else {
        this.searchResults = [];
      }
    },
    applyFilter() {
    },
    editDish(dish) {
      this.editDishData.id = dish.id;
      this.editDishData.name = dish.name;
      this.editDishData.image = null; // 清空当前图片
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    handleImageChange(event) {
      this.editDishData.image = event.target.files[0];
    },
    async updateDish() {
      const { id, name, image } = this.editDishData;
      const result = await updateDish(id, name, image);
      if (result && result.message === 'Update successful') {
        this.fetchUserDishes();
        this.fetchFavouriteDishes();
        this.closeEditModal();
      } else {
        alert('更新失败');
      }
    },
    openAddIngredientsModal() {
      this.newIngredients = [{ name: '', quantity: '', unit: '' }];
      this.showAddIngredientsModal = true;
    },
    closeAddIngredientsModal() {
      this.showAddIngredientsModal = false;
    },
    addIngredientField() {
      this.newIngredients.push({ name: '', quantity: '', unit: '' });
    },
    async submitNewIngredients() {
      const payload = {
        uid: this.userId,
        did: this.currentDishId,
        ingredients: this.newIngredients.map(ingredient => ({
          ...ingredient,
          quantity: Number(ingredient.quantity) // 确保数量是数字类型
        }))
      };

      const result = await addIngredients(payload);
      if (result) {
        this.viewIngredients({ id: this.currentDishId }); // 重新加载食材信息
        this.closeAddIngredientsModal();
      } else {
        alert('添加食材失败');
      }
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

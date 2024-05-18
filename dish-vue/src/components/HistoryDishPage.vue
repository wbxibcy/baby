<template>
  <div class="history-dish-page">
    <el-card class="content-card">
      <h2>历史宝宝辅食</h2>

      <el-form inline>
        <el-form-item label="显示">
          <el-select v-model="filter" @change="applyFilter" placeholder="请选择">
            <el-option label="全部" value="all"></el-option>
            <el-option label="收藏" value="favourite"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="搜索" class="search-item">
          <el-input v-model="searchQuery" placeholder="搜索菜品..."></el-input>
        </el-form-item>
        <el-form-item class="search-button">
          <el-button @click="searchDishes" type="primary">搜索</el-button>
        </el-form-item>
      </el-form>

      <div class="dish-list">
        <div class="dish-item" v-for="dish in paginatedDishes" :key="dish.id">
          <el-image v-if="dish.image" :src="'data:image/jpeg;base64,' + dish.image" class="dish-image" @click="viewIngredients(dish)" />
          <div class="dish-info">
            <span class="dish-name">{{ dish.name }}</span>
            <div class="dish-actions">
              <el-button @click="confirmDelete(dish.id)" type="danger" plain>删除</el-button>
              <el-button @click="editDish(dish)" type="warning" plain>编辑</el-button>
            </div>
          </div>
        </div>
      </div>

      <el-pagination
        layout="prev, pager, next"
        :total="filteredDishes.length"
        :page-size="3"
        @current-change="handlePageChange"
        v-model:currentPage="currentPage">
      </el-pagination>

      <el-dialog v-model="showModal" title="食材信息">
        <ul>
          <li v-for="ingredient in ingredients" :key="ingredient.name">
            <span>{{ ingredient.name }}: {{ ingredient.quantity }} {{ ingredient.unit }}</span>
          </li>
        </ul>
        <template #footer>
          <el-button @click="closeModal">关闭</el-button>
          <!-- <el-button type="primary" @click="openAddIngredientsModal">继续添加食材</el-button> -->
        </template>
      </el-dialog>

      <el-dialog v-model="showEditModal" title="编辑菜品">
        <el-form>
          <el-form-item label="名字">
            <el-input v-model="editDishData.name"></el-input>
          </el-form-item>
          <el-form-item label="图片">
            <input type="file" @change="handleImageChange" />
          </el-form-item>
          <div v-for="(ingredient, index) in editDishData.ingredients" :key="index" class="ingredient">
            <el-form-item label="食材名字">
              <el-input v-model="ingredient.name"></el-input>
            </el-form-item>
            <el-form-item label="数量">
              <el-input v-model="ingredient.quantity" type="number"></el-input>
            </el-form-item>
            <el-form-item label="单位">
              <el-input v-model="ingredient.unit"></el-input>
            </el-form-item>
          </div>
        </el-form>
        <template #footer>
          <el-button @click="closeEditModal">关闭</el-button>
          <el-button type="primary" @click="updateDish">更新</el-button>
        </template>
      </el-dialog>

      <el-dialog v-model="showAddIngredientsModal" title="添加食材">
        <div v-for="(ingredient, index) in newIngredients" :key="index">
          <el-form-item label="食材名字">
            <el-input v-model="ingredient.name"></el-input>
          </el-form-item>
          <el-form-item label="数量">
            <el-input v-model="ingredient.quantity" type="number"></el-input>
          </el-form-item>
          <el-form-item label="单位">
            <el-input v-model="ingredient.unit"></el-input>
          </el-form-item>
        </div>
        <template #footer>
          <el-button @click="addIngredientField">添加更多食材</el-button>
          <el-button type="primary" @click="submitNewIngredients">提交</el-button>
          <el-button @click="closeAddIngredientsModal">关闭</el-button>
        </template>
      </el-dialog>

      <el-dialog v-model="showDeleteConfirmDialog" title="确认删除">
        <p>你确定要删除这个菜品吗？此操作不可恢复。</p>
        <template #footer>
          <el-button @click="showDeleteConfirmDialog = false">取消</el-button>
          <el-button type="primary" @click="deleteConfirmedDish">确认删除</el-button>
        </template>
      </el-dialog>
    </el-card>
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
      showDeleteConfirmDialog: false,
      ingredients: [],
      currentDishId: null,
      dishIdToDelete: null,
      editDishData: {
        id: null,
        name: '',
        image: null,
        ingredients: []
      },
      newIngredients: [
        { name: '', quantity: '', unit: '' }
      ],
      currentPage: 1,
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
    },
    paginatedDishes() {
      const start = (this.currentPage - 1) * 3;
      const end = start + 3;
      return this.filteredDishes.slice(start, end);
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
    confirmDelete(dishId) {
      this.dishIdToDelete = dishId;
      this.showDeleteConfirmDialog = true;
    },
    async deleteConfirmedDish() {
      await deleteDish(this.dishIdToDelete);
      this.showDeleteConfirmDialog = false;
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
    async editDish(dish) {
      this.editDishData.id = dish.id;
      this.editDishData.name = dish.name;
      this.editDishData.image = null; // 清空当前图片
      this.editDishData.ingredients = await fetchIngredients(this.userId, dish.id);
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    handleImageChange(event) {
      this.editDishData.image = event.target.files[0];
    },
    async updateDish() {
      const { id, name, image, ingredients } = this.editDishData;
      const result = await updateDish(id, name, image, ingredients);
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
    },
    handlePageChange(page) {
      this.currentPage = page;
    }
  },
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background-image: url('../assets/history-background.png'); /* 替换为你的背景图片路径 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  overflow: hidden;
}

.history-dish-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Ensures the container takes the full height of the viewport */
  padding: 20px;
  box-sizing: border-box;
}

.content-card {
  background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent background to ensure content readability */
  padding: 20px;
  border-radius: 10px;
  width: 100%;
  max-width: 600px;
}

.el-form-item.search-item,
.el-form-item.search-button {
  margin-bottom: 0;
}

.dish-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.dish-item {
  display: flex;
  align-items: center;
  border: 1px solid #e0e0e0;
  padding: 10px;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.dish-image {
  margin-right: 15px;
  cursor: pointer;
  border-radius: 5px;
}

.dish-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dish-name {
  font-size: 18px;
  font-weight: bold;
}

.dish-actions {
  display: flex;
  gap: 10px;
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

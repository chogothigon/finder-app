<template>
  <div class="search-bar">
    <div class="field-group">
      <label for="make">Make</label>
      <select id="make">
        <option 
        v-for="make in uniqueMakes" :key="make" :value="make">{{ make }}
        </option>
      </select>
    </div>

    <div class="field-group">
      <label for="model">Model</label>
      <select id="model">
        <option 
        v-for="model in uniqueModels" :key="model" :value="model">{{ model }}
        </option>
      </select>
    </div>


    <div class="field-group">
      <label for="zip">ZIP</label>
      <input type="text" id="zip">
    </div>

    <button>Search</button>

  </div>

  
</template>

<script>
export default {
  name: 'SearchBar'
}
</script>

<style scoped>
.search-bar {
  width: 95%;
  margin: 20px auto;
  padding: 24px;
  border: 1px solid #d9d9d9;
  border-radius: 16px;
  background-color: white;
  box-sizing: border-box;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 30px;
}

.field-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

label {
  font-size: 1.2rem;
  font-weight: 500;
  color: #2c3e50;
}

select,
input {
  font-size: 1.1rem;
  padding: 10px 14px;
  border: 1px solid #d9d9d9;
  border-radius: 10px;
  background-color: white;
  color: #2c3e50;
}
</style>
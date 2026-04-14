<template>
  <div class="search-bar">
    <div class="main-fields">
      <div class="field-group">
        <label for="make">Make</label>
        <select id="make" v-model="selectedMake">
          <option value="">Select</option>
          <option 
          v-for="make in uniqueMakes" :key="make" :value="make">{{ make }}
          </option>
        </select>
      </div>
    
    <div class="field-group">
      <label for="model">Model</label>
      <select id="model" v-model="selectedModel">
        <option value="">Select</option>
        <option 
        v-for="model in uniqueModels" :key="model" :value="model">{{ model }}
        </option>
      </select>
    </div>

    <div class="field-group">
      <label for="year">Year</label>
      <select id="year" v-model="selectedYear">
        <option value="">Select</option>
        <option
        v-for="year in uniqueYears" :key="year" :value="year">{{ year }}
        </option>
      </select>
    </div>


    <div class="field-group">
      <label for="zip">ZIP</label>
      <input type="text" id="zip" v-model="selectedZIP" list="zip-list" placeholder="Enter">
      <datalist id="zip-list">
        <option v-for="zip in uniqueZIPs" :key="zip" :value="zip">{{ zip }}</option>
      </datalist>
    </div>

    <button @click="doSearch">Search</button>
    </div>

    <div class="advanced-wrap">
      <button @click="isAdvanced = !isAdvanced" class="advanced-toggle">
        Advanced {{ isAdvanced ? '▴' : '▾' }}
      </button>

      <div v-if="isAdvanced" class="advanced-panel">

        <div class="advanced-fields">

          <div class="advanced-inline">
            <span class="advanced-label">Advanced:</span>

            <div class="sort-toggles">
              <button
                type="button"
                class="sort-toggle"
                :class="{ active: sortOrder === 'newest' }"
                @click="sortOrder = 'newest'"
              >
                Newest Arrival
              </button>

              <button
                type="button"
                class="sort-toggle"
                :class="{ active: sortOrder === 'oldest' }"
                @click="sortOrder = 'oldest'"
              >
                Oldest Arrival
              </button>

              <button
                type="button"
                class="sort-toggle"
                :class="{ active: sortOrder === 'year-newest' }"
                @click="sortOrder = 'year-newest'"
              >
                Newest Year
              </button>

              <button
                type="button"
                class="sort-toggle"
                :class="{ active: sortOrder === 'year-oldest' }"
                @click="sortOrder = 'year-oldest'"
              >
                Oldest Year
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  data() {
    return {
      cars: [],
      uniqueMakes: [],
      uniqueModels: [],
      uniqueYears: [],
      uniqueZIPs: [],
      selectedMake: '',
      selectedModel: '',
      selectedYear: '',
      selectedZIP: '',
      sortOrder: 'newest',
      isAdvanced: false
    }
  },
  
   async mounted() {
    try {
      console.log('SearchBar mounted')

      const response = await fetch('/api/cars')
      console.log('response ok:', response.ok)

      const data = await response.json()
      console.log('data:', data)

      this.cars = data

      const makes = data.map(car => car.car_make).filter(Boolean)
      console.log('makes:', makes)
      this.uniqueMakes = [...new Set(makes)].sort()
      console.log('uniqueMakes:', this.uniqueMakes)

      const years = data.map(car => car.car_year).filter(Boolean)
      this.uniqueYears = [...new Set(years)].sort((a, b) => b - a)

      const models = data.map(car => car.car_model).filter(Boolean)
      this.uniqueModels = [...new Set(models)].sort()

      const zips = data.map(car => car.junkyard_zip).filter(Boolean)
      this.uniqueZIPs = [...new Set(zips)].sort()

    } catch (err) {
      console.error('Error loading makes:', err)
    }
  },
  watch: {
  selectedMake(newMake) {
    if (!newMake) {
      const allModels = this.cars
        .map(car => car.car_model)
        .filter(Boolean)
      this.uniqueModels = [...new Set(allModels)].sort()

      const allYears = this.cars
        .map(car => car.car_year)
        .filter(Boolean)
      this.uniqueYears = [...new Set(allYears)].sort((a, b) => b - a)

      return
    }

    const models = this.cars
      .filter(car => car.car_make === newMake)
      .map(car => car.car_model)
      .filter(Boolean)
    this.uniqueModels = [...new Set(models)].sort()

    const years = this.cars
      .filter(car => car.car_make === newMake)
      .map(car => car.car_year)
      .filter(Boolean)
    this.uniqueYears = [...new Set(years)].sort((a, b) => b - a)

    if (this.selectedModel && !this.uniqueModels.includes(this.selectedModel)) {
      this.selectedModel = ''
    }

    if (this.selectedYear && !this.uniqueYears.includes(parseInt(this.selectedYear))) {
      this.selectedYear = ''
    }
  },

  selectedModel(newModel) {
    if (!this.selectedMake) return

    if (!newModel) {
      const years = this.cars
        .filter(car => car.car_make === this.selectedMake)
        .map(car => car.car_year)
        .filter(Boolean)
      this.uniqueYears = [...new Set(years)].sort((a, b) => b - a)

      return
    }

    const years = this.cars
      .filter(car => car.car_make === this.selectedMake && car.car_model === newModel)
      .map(car => car.car_year)
      .filter(Boolean)
    this.uniqueYears = [...new Set(years)].sort((a, b) => b - a)

    if (this.selectedYear && !this.uniqueYears.includes(parseInt(this.selectedYear))) {
      this.selectedYear = ''
    }
  }
},

methods: {
  doSearch() {
    this.$emit('search', {
      make: this.selectedMake,
      model: this.selectedModel,
      year: this.selectedYear,
      zip: this.selectedZIP,
      sort: this.sortOrder
    })
  }
}
}
</script>

<style scoped>
.search-bar {
  width: 95%; 
  margin: 20px auto;
  padding: 28px 32px;
  border: 1px solid #d9d9d9;
  border-radius: 16px;
  background-color: white;
  box-sizing: border-box;
}

.main-fields {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: flex-end;
  justify-content: center;
}

.main-fields button {
  align-self: flex-end;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 1.2rem;
  font-weight: 500;
  color: #2c3e50;
}

select, input{
  font-size: 1.05rem;
  padding: 10px 14px;
  border: 1px solid #d9d9d9;
  border-radius: 10px;
  background-color: white;
  color: #2c3e50;
  width: 170px;
  box-sizing: border-box;
}

button {
  font-size: 1rem;
  padding: 10px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 10px;
  background-color: #2c3e50;
  color: white;
  cursor: pointer;
}

.advanced-wrap {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #ececec;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.advanced-toggle {
  font-size: 0.92rem;
  padding: 0;
  border: none;
  background: transparent;
  color: #5c6773;
  cursor: pointer;
}

.advanced-toggle:hover {
  text-decoration: underline;
}

.advanced-panel {
  margin-top: 10px;
}



.advanced-fields {
  margin-top: 10px;
}

.advanced-inline {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.advanced-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #5c6773;
}

.sort-toggles {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.sort-toggle {
  font-size: 0.9rem;
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 999px;
  background: white;
  color: #2c3e50;
  cursor: pointer;
}

.sort-toggle.active {
  background: #2c3e50;
  color: white;
  border-color: #2c3e50;
}
</style>
<!--
    About cards will be made for each team member, showing their name, a photo, and a small description.
-->
<template>
  <div class="about-card">
    <img :src="pic" :alt="name" class="profile-pic" />
    <div class="card-content">
      <h3 class="name">{{ name }}</h3>
      <p class="description">{{ description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutCard',
  props: {
    name: {
      type: String,
      required: true
    },
    pic: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
 
  }
}
</script>

<style scoped>
.about-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-pic {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}

.card-content {
  flex: 1;
}

.name {
  margin: 0 0 10px 0;
  font-size: 1.3em;
  color: #333;
}

.description {
  margin: 0 0 10px 0;
  color: #666;
  line-height: 1.4;
}


</style>
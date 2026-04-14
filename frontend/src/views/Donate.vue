<template>
  <section>
    <h2>Thank you for supporting Purple Team!</h2>
    <div class="donate-container">
      <a href="https://youtu.be/XfELJU1mRMg?si=UoQ9OD9i45DnECgx" target="_blank">
        <img :src="patreonPic" alt="Patreon" class="patreon-button" />
      </a>
    </div>
  </section>
</template>

<script>

import patreonPic from '@/assets/patreon.png';

export default {
  name: 'DonateView',
  data() {
    return {
      patreonPic
    }
  }
}
</script>

<style scoped>
.donate-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh;
  margin-top: 20px;
}

.patreon-button {
  width: 400px;
  height: auto;
  cursor: pointer;
  transition: transform 0.2s;
}

.patreon-button:hover {
  transform: scale(1.05);
}
</style>
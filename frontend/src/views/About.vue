<template>
  <section>
    <h2>Meet the Team</h2>
    <div class="team-section">
      
      <div class="team-cards">
        <AboutCard
          name="Ryan"
          pic="../assets/ryan.jpg"
          description="Description"
          fun="Fun fact"
        />
        <AboutCard
          name="Reese"
          pic="/placeholder.jpg"
          description="Description"
          fun="Fun fact"
        />
        <AboutCard
          name="Kimball"
          pic="/placeholder.jpg"
          description="Description"
          fun="Fun fact"
        />
        <AboutCard
          name="Maya"
          pic="/placeholder.jpg"
          description="Description"
          fun="Fun fact"
        />
        <AboutCard
          name="Sam"
          pic="/placeholder.jpg"
          description="Description"
          fun="Fun fact"
        />
      </div>
    </div>
  </section>
</template>

<script>
import AboutCard from '@/components/AboutCard.vue';

export default {
  name: 'AboutView',
  components: {AboutCard}
}
</script>

<style scoped>
.team-section {
  margin-top: 2rem;
}

.team-section h3 {
  text-align: center;
  margin-bottom: 2rem;
}

.team-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

@media (max-width: 768px) {
  .team-cards {
    flex-direction: column;
    align-items: center;
  }
}
</style>
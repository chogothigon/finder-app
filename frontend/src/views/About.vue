<template>
  <section>
    <h2>Meet the Team</h2>
    <div class="team-section">
      
      <div class="team-cards">
        <AboutCard
          name="Ryan"
          :pic="ryanPic"
          description="Your network security is my priority. My network? Ongoing research project."
        
        />
        <AboutCard
          name="Reese"
          pic="/placeholder.jpg"
          description="I like working on fun cybersecurity projects!"
          
        />
        <AboutCard
          name="Kimball"
          pic="/placeholder.jpg"
          description="I love cybersecurity!"
          
        />
        <AboutCard
          name="Maya"
          :pic="mayaPic"
          description="I like working on things that make a difference!"
          
        />
        <AboutCard
          name="Sam"
          :pic="samPic"
          description="Interested in malware research and cyber threat intelligence"
          
        />
      </div>
    </div>
  </section>
</template>

<script>
import AboutCard from '@/components/AboutCard.vue';
import ryanPic from '@/assets/ryan.jpg';
import samPic from '@/assets/sam.png';
import mayaPic from '@/assets/maya.jpg';

export default {
  name: 'AboutView',
  components: {AboutCard},
  data() {
    return {
      ryanPic,
      samPic,
      mayaPic
    }
  }
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

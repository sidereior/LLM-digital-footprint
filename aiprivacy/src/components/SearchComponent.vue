<!-- src/components/SearchComponent.vue -->
<template>
  <div>
    <input v-model="name" placeholder="Enter your name">
    <button @click="search">Search</button>
    <div v-if="output">{{ output }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      output: ''
    }
  },
  methods: {
    async search() {
      if (this.name) {
        try {
          let response = await fetch('http://localhost:5000/api/search', {
             method: 'POST',
            headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: this.name })
          });
                   if (response.ok) {
            let data = await response.json();
            this.output = data.result;
          } else {
            console.error('Server error:', response.status);
          }
        } catch (error) {
          console.error('Network error:', error);
        }
      }
    }
  }
}
</script>

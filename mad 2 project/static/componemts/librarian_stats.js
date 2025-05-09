export default {
    template: `
      <div class="container mt-5" v-cloak>
        <div>
          <h1>Librarian Stats</h1>
          <div v-if="loading">Loading...</div>
          <div v-else>
            <h2>Section Distribution (Pie Chart)</h2>
            <img :src="sectionChart" alt="Section Pie Chart" />
            
          </div>
        </div>
      </div>
    `,
    data() {
      return {
        sectionChart: '',
        loading: true,
        token: localStorage.getItem('auth-token'),
      };
    },
    async mounted() {
      try {
        const response = await fetch('/librarian_stats', {
          headers: {
            'Authentication-Token': this.token,
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        this.sectionChart = `data:image/png;base64,${data.section_chart}`;
      } catch (error) {
        console.error('Error fetching librarian stats:', error);
      } finally {
        this.loading = false;
      }
    },
  };
  
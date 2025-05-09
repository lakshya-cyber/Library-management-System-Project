export default {
  template: `
    <div>
      <div class="container mt-5 text-center">
        <h1>Welcome to Book Haven</h1>
        <div class="my-4">
          <img class="img-fluid" src="../../static/assets/andy-vult-xdFzD2_iP9A-unsplash.jpg" alt="logo" width="500px" height="300">
        </div>
        <div>
          <button @click="downloadResource" class="btn btn-primary">Download Details</button>
          <span v-if="isWaiting" class="text-muted">Please wait...</span>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      isWaiting: false,
    }
  },
  methods: {
    async downloadResource() {
      this.isWaiting = true
      const res = await fetch('/download-csv')
      const data = await res.json()
      if (res.ok) {
        const taskId = data['task-id']
        const intv = setInterval(async () => {
          const csv_res = await fetch(`/get-csv/${taskId}`)
          if (csv_res.ok) {
            this.isWaiting = false
            clearInterval(intv)
            window.location.href = `/get-csv/${taskId}`
            alert("CSV file is ready for download!");
          }
        }, 1000)
      }
    },
  },
}

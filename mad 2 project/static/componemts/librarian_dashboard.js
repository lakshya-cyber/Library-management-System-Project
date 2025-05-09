export default {
    template: `
      <div>
        <div class="container mt-5">
          <div class="row justify-content-center mt-4">
            <div class="col-md-6">
              <div class="card">
                <div class="card-header">
                </div>
                <img class="card-img-bottom" src="../../static/assets/gabriel-sollmann-Y7d265_7i08-unsplash.jpg" alt="logo" width="500px" height="300">
                <br>
                <button @click="addSection" class="btn btn-primary mt-4 mb-4 col-12">Add section</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `,
    methods: {
      addSection() {
        this.$router.push({ path: '/add_section' });
      }
    }
  }
  
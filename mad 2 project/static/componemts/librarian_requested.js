export default {
  template: `
    <div class="container">
      <h1>User - Requests</h1>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th>Book Name</th>
            <th>User</th>
            <th>Days Requested</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr  v-if="request.status == 0" v-for="request in requested_books" :key="request.book_id">
            
              <td>{{ request.book_name }}</td>
              <td>{{ request.user_email }}</td>
              <td>{{ request.days_requested }}</td>
              <td>
                <button @click="approveRequest(request.book_id)" class="btn btn-success">Approve</button>
                <button @click="rejectRequest(request.book_id)" class="btn btn-danger">Reject</button>
              </td>
          
          </tr>
        </tbody>
      </table>
    </div>
  `,
  data() {
    return {
      requested_books: [],
      token: localStorage.getItem('auth-token'),
      error: null,
    };
  },
  methods: {
    async approveRequest(book_id) {
      try {
        const res = await fetch(`/approve_request/${book_id}`, {
          method: 'POST',
          headers: {
            'Authentication-Token': this.token,
          },
        });

        if (!res.ok) {
          const errorData = await res.json();
          this.error = errorData.message || 'An error occurred';
          return;
        }

        // Update the list of requested books after approval
        this.fetchRequestedBooks();
      } catch (e) {
        this.error = 'An error occurred while approving the request';
      }
    },
    async rejectRequest(book_id) {
      try {
        const res = await fetch(`/reject_request/${book_id}`, {
          method: 'POST',
          headers: {
            'Authentication-Token': this.token,
          },
        });

        if (!res.ok) {
          const errorData = await res.json();
          this.error = errorData.message || 'An error occurred';
          return;
        }

        // Update the list of requested books after rejection
        this.fetchRequestedBooks();
      } catch (e) {
        this.error = 'An error occurred while rejecting the request';
      }
    },
    async fetchRequestedBooks() {
      try {
        const res = await fetch('/requested_books', {
          headers: {
            'Authentication-Token': this.token,
          },
        });

        if (!res.ok) {
          this.error = `Error: ${res.statusText}`;
          return;
        }

        const data = await res.json();
        this.requested_books = data;
      } catch (e) {
        this.error = 'An error occurred while fetching the data';
      }
    },
  },
  mounted() {
    this.fetchRequestedBooks();
  },
};

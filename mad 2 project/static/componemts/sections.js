// export default {
//   template: `
//     <div>
//       <div class="container">
//         <div class="col-md-6 ">
//           <button @click="addSection" class="btn btn-primary mt-4 mb-4">Add section</button>
//         </div>
//         <div class="row">
//           <div v-for="section in sections" :key="section.section_id" class="col-md-6">
//             <div v-if="error">{{ error }}</div>
//             <table class="bg-success justify-content-center">
//               <tr>
//                 <td><router-link :to="{ name: 'book_summary', params: { section_id: section.section_id } }">Books</router-link></td>
                
//               </tr>
//               <tr>
//                 <td>ID:</td>
//                 <td>{{ section.section_id }}</td>
//               </tr>
//               <tr>
//                 <td>Title:</td>
//                 <td>{{ section.name }}</td>
//               </tr>
//               <tr>
//                 <td>Description:</td>
//                 <td>{{ section.description }}</td>
//               </tr>
//               <tr>
//                 <td><button @click="updateSection(section)" class="btn btn-primary">Update</button></td>
//                 <td><button @click="addBook(section)" class="btn btn-danger">Add book</button></td>
//               </tr>
//               <tr>
//                 <td><button @click="deleteSection(section.section_id)" class="btn btn-danger">Delete</button></td>
//               </tr>
//             </table>
//           </div>
//         </div>
//       </div>
//     </div>
//   `,
//   data() {
//     return {
//       sections: [],
//       token: localStorage.getItem('auth-token'),
//       error: null,
//     };
//   },
//   methods: {
//     addBook(section) {
//       this.$router.push({ name: 'add_book', params: { section_id: section.section_id,section_name: section.name } });
//     },
//     updateSection(section) {
//       this.$router.push({ name: 'update_section', params: { section_id: section.section_id,section_name: section.name,section_description: section.description } });
//     },
//     deleteSection(section_id) {
//       fetch(`/delete_section/${section_id}`, {
//         method: 'DELETE',
//         headers: {
//           'Authentication-Token': this.token,
//         },
//       })
//       },
//     addSection() {
//       this.$router.push({ path: '/add_section' });
//     },
//   },
// async mounted() {

//     const res = await fetch('/sections',{
//       headers:{
//        'Authentication-Token': this.token,
//       },
//     })

//     const data = await res.json().catch((e)=>{})
//     if(res.ok){
//         this.sections = data
//     }else{
//       this.error = res.status
//     }
//   }
// };

export default {
  template: `
    <div class="container mt-5">
    <div class="d-flex justify-content-between mb-4">
      <button @click="addSection" class="btn btn-primary">Add Section</button>
      <div class="d-flex col-md-6">
        <input v-model="searchQuery" @input="filterSections" placeholder="Search sections" class="form-control me-2" />
        <button @click="filterSections" class="btn btn-primary">Search</button>
      </div>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <table class="table table-bordered table-hover table-dark">
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Description</th>
          <th>Books</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="section in filteredSections" :key="section.section_id">
          <td>{{ section.section_id }}</td>
          <td>{{ section.name }}</td>
          <td>{{ section.description }}</td>
          <td>
            <button @click="seebooks(section.section_id)" class="btn btn-primary btn-sm me-2">Books</button>
          </td>
          <td>
            <button @click="updateSection(section)" class="btn btn-primary btn-sm me-2">Update</button>
            <button @click="addBook(section)" class="btn btn-success btn-sm me-2">Add Book</button>
            <button @click="deleteSection(section.section_id)" class="btn btn-danger btn-sm">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  `,
  data() {
    return {
      sections: [],
      searchQuery: '',
      filteredSections: [],
      token: localStorage.getItem('auth-token'),
      error: null,
    };
  },
  methods: {
    addBook(section) {
      this.$router.push({ name: 'add_book', params: { section_id: section.section_id, section_name: section.name } });
    },
    seebooks(section_id) {
      this.$router.push({ name: 'book_summary', params: { section_id } });
    },
    updateSection(section) {
      this.$router.push({ name: 'update_section', params: { section_id: section.section_id, section_name: section.name, section_description: section.description } });
    },
    async deleteSection(section_id) {
      try {
        const res = await fetch(`/delete_section/${section_id}`, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': this.token,
          },
        });

        if (!res.ok) {
          const errorData = await res.json();
          this.error = errorData.message || 'An error occurred';
          return;
        }

        // Remove the deleted section from the list
        this.sections = this.sections.filter(section => section.section_id !== section_id);
        this.filteredSections = this.sections; // Update filteredSections after deletion
      } catch (e) {
        this.error = 'An error occurred while deleting the section';
      }
    },
    addSection() {
      this.$router.push({ path: '/add_section' });
    },
    filterSections() {
      this.filteredSections = this.sections.filter(section =>
        section.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        section.description.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  async mounted() {
    const res = await fetch('/sections', {
      headers: {
        'Authentication-Token': this.token,
      },
    });

    const data = await res.json().catch((e) => {});
    if (res.ok) {
      this.sections = data;
      this.filteredSections = data; // Initialize filteredSections with all sections
    } else {
      this.error = res.status;
    }
  }
};


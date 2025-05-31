document.addEventListener("DOMContentLoaded", () => {
  const API_BASE_URL = "http://localhost:5000/api"; // Adjust if your backend runs elsewhere

  const authLinkLogin = document.getElementById("auth-link-login");
  const authLinkRegister = document.getElementById("auth-link-register");
  const authLinkLogout = document.getElementById("auth-link-logout");
  const authLinkProfile = document.getElementById("auth-link-profile");

  const featuredCoursesGrid = document.getElementById("featured-courses-grid");

  // Function to update navigation based on authentication status
  function updateNav() {
    const token = localStorage.getItem("authToken");
    const user = JSON.parse(localStorage.getItem("authUser"));

    if (token && user) {
      if (authLinkLogin) authLinkLogin.style.display = "none";
      if (authLinkRegister) authLinkRegister.style.display = "none";
      if (authLinkLogout) authLinkLogout.style.display = "inline";
      if (authLinkProfile) authLinkProfile.style.display = "inline";
      if (authLinkProfile)
        authLinkProfile.textContent = user.username || "Profile";
    } else {
      if (authLinkLogin) authLinkLogin.style.display = "inline";
      if (authLinkRegister) authLinkRegister.style.display = "inline";
      if (authLinkLogout) authLinkLogout.style.display = "none";
      if (authLinkProfile) authLinkProfile.style.display = "none";
    }
  }

  // Handle logout
  if (authLinkLogout) {
    authLinkLogout.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("authToken");
      localStorage.removeItem("authUser");
      updateNav();
      // Redirect to home or login page
      if (
        window.location.pathname !== "/index.html" &&
        window.location.pathname !== "/"
      ) {
        window.location.href = "index.html";
      }
    });
  }

  // Fetch and display featured courses (placeholder)
  async function fetchFeaturedCourses() {
    if (!featuredCoursesGrid) return;

    featuredCoursesGrid.innerHTML = "<p>Loading courses...</p>"; // Show loading message

    try {
      const response = await fetch(`${API_BASE_URL}/courses`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const courses = await response.json();

      featuredCoursesGrid.innerHTML = ""; // Clear loading message or old content

      if (!courses || courses.length === 0) {
        featuredCoursesGrid.innerHTML =
          "<p>No courses available at the moment. Check back soon!</p>";
        return;
      }

      courses.forEach((course) => {
        const courseCard = `
                <div class="course-card">
                    <img src="images/fd.jpg" alt="${
                      course.title || "Course image"
                    }">
                    <h3>${course.title || "N/A"}</h3>
                    <p>${(
                      course.description || "No description available."
                    ).substring(0, 100)}${
          course.description && course.description.length > 100 ? "..." : ""
        }</p>
                    <p><em>Instructor ID: ${
                      course.instructor_id || "N/A"
                    }</em></p>
                    <a href="course_view.html?id=${
                      course.id
                    }" class="btn btn-primary">View Course</a>
                </div>
            `;
        // Note: Using a placeholder image "images/fd.jpg" and "Instructor ID" as instructor name is not available directly.
        // You might want to fetch instructor details separately or include them in the /courses API response.
        featuredCoursesGrid.insertAdjacentHTML("beforeend", courseCard);
      });
    } catch (error) {
      console.error("Failed to fetch courses:", error);
      if (featuredCoursesGrid) {
        featuredCoursesGrid.innerHTML =
          '<p class="error-message">Could not load courses. Please try again later.</p>';
      }
    }
  }

  // function renderCourses(courses) {
  //     if (!featuredCoursesGrid) return;
  //     featuredCoursesGrid.innerHTML = ''; // Clear existing
  //     if (!courses || courses.length === 0) {
  //         featuredCoursesGrid.innerHTML = '<p>No featured courses available at the moment.</p>';
  //         return;
  //     }
  //     courses.forEach(course => {
  //         const courseCard = `
  //             <div class="course-card">
  //                 <img src="${course.imageUrl || 'images/course-placeholder.png'}" alt="${course.title}">
  //                 <h3>${course.title}</h3>
  //                 <p>${course.shortDescription || course.description.substring(0,100)}...</p>
  //                 <a href="course_view.html?id=${course.id}" class="btn btn-primary">View Details</a>
  //             </div>
  //         `;
  //         featuredCoursesGrid.insertAdjacentHTML('beforeend', courseCard);
  //     });
  // }

  // Initial setup
  updateNav();
  if (document.body.contains(featuredCoursesGrid)) {
    // Only call if the element exists on the page
    fetchFeaturedCourses();
  }

  // Expose functions to global scope if needed for inline event handlers (not recommended)
  // window.handleLogout = logout;

  // Add more page-specific logic as needed, e.g., for login form, registration form, etc.
  // Example: if (document.getElementById('login-form')) { initLoginForm(); }
});

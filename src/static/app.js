/**
 * Mergington High School Activities – Frontend Application
 *
 * This script fetches extracurricular activities from the backend API and
 * renders them on the page.  It also handles the student sign-up form,
 * posting the selected activity and email to the server and displaying a
 * success or error message to the user.
 */

document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  /**
   * Fetch all activities from the API and render them on the page.
   *
   * Each activity is displayed as a card showing its name, description,
   * schedule, and the number of spots still available.  Activity names are
   * also added to the sign-up form's dropdown so students can select one.
   *
   * @async
   * @returns {Promise<void>}
   */
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  /**
   * Display a feedback message to the user and automatically hide it after
   * five seconds.
   *
   * @param {string} text                          - The message text to display.
   * @param {("success"|"error"|"info")} cssClass  - CSS class that controls the
   *   colour and style of the message box.
   */
  function showMessage(text, cssClass) {
    messageDiv.textContent = text;
    messageDiv.className = cssClass;
    messageDiv.classList.remove("hidden");

    // Hide message after 5 seconds
    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  }

  /**
   * Handle sign-up form submission.
   *
   * Reads the student's email and chosen activity from the form, sends a POST
   * request to the API, and shows a success or error message based on the
   * server response.
   *
   * @async
   * @param {SubmitEvent} event - The form submit event.
   * @returns {Promise<void>}
   */
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        signupForm.reset();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to sign up. Please try again.", "error");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app by loading activities on page load
  fetchActivities();
});

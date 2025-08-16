const form = document.getElementById("contact-form");
const submitBtn = document.getElementById("contact-form-submit-btn");
const submitText = document.getElementById("contact-form-submit-text");
const submitSpinner = document.getElementById("contact-form-submit-spinner");
const alertContainer = document.getElementById("contact-form-alert-container");

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  // Clear previous errors and alerts
  clearErrors();
  clearAlerts();

  // Show loading state
  setLoadingState(true);

  // Get form data
  const formData = {
    name: document.getElementById("id_name").value.trim(),
    email: document.getElementById("id_email").value.trim(),
    subject: document.getElementById("id_subject").value.trim(),
    message: document.getElementById("id_message").value.trim(),
  };

  try {
    const response = await fetch("/core/mail/us/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const data = await response.json();

    if (data.success) {
      // Show success message
      showAlert("success", data.message);

      // Reset form
      form.reset();
    } else {
      // Show error message
      showAlert("danger", data.message);

      // Display field-specific errors if they exist
      if (data.errors) {
        displayFieldErrors(data.errors);
      }
    }
  } catch (error) {
    console.error("Error:", error);
    showAlert(
      "danger",
      "An error occurred while sending your message. Please try again."
    );
  } finally {
    // Hide loading state
    setLoadingState(false);
  }
});

function setLoadingState(loading) {
  if (loading) {
    submitBtn.disabled = true;
    submitText.textContent = "Sending...";
    submitSpinner.style.display = "inline-block";
  } else {
    submitBtn.disabled = false;
    submitText.textContent = "Send Message";
    submitSpinner.style.display = "none";
  }
}

function showAlert(type, message) {
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show text-center`;
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
  alertContainer.appendChild(alertDiv);

  // Auto-dismiss success alerts after 5 seconds
  if (type === "success") {
    setTimeout(() => {
      if (alertDiv.parentNode) {
        alertDiv.remove();
      }
    }, 5000);
  }
}

function clearAlerts() {
  alertContainer.innerHTML = "";
}

function displayFieldErrors(errors) {
  Object.keys(errors).forEach((field) => {
    const errorDiv = document.getElementById(`${field}-error`);
    const inputField = document.getElementById(`id_${field}`);

    if (errorDiv && inputField) {
      errorDiv.textContent = errors[field].join(", ");
      errorDiv.style.display = "block";
      inputField.classList.add("is-invalid");
    }
  });
}

function clearErrors() {
  // Clear all error messages and invalid states
  const errorDivs = document.querySelectorAll(
    "#contact-form .invalid-feedback"
  );
  const inputFields = document.querySelectorAll("#contact-form .form-control");

  errorDivs.forEach((div) => {
    div.textContent = "";
    div.style.display = "none";
  });

  inputFields.forEach((field) => {
    field.classList.remove("is-invalid");
  });
}

// Real-time validation - clear errors when user starts typing
const inputFields = document.querySelectorAll("#contact-form .form-control");
inputFields.forEach((field) => {
  field.addEventListener("input", function () {
    if (this.classList.contains("is-invalid")) {
      this.classList.remove("is-invalid");
      const errorDiv = document.getElementById(`${this.name}-error`);
      if (errorDiv) {
        errorDiv.textContent = "";
        errorDiv.style.display = "none";
      }
    }
  });
});

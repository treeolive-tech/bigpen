"use client";

import { useState } from "react";

// Define the structure of form data that users will input
interface FormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

// Define the structure of alert messages (success or error notifications)
interface Alert {
  id: number; // corresponds to the Date time that the aleart appears
  type: "success" | "danger";
  message: string;
}

// Define the structure of validation errors returned from the server
interface Errors {
  [key: string]: string | string[];
}

export default function EmailUsForm() {
  // Store the current form input values
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  // Track whether the form is currently being submitted (to show loading state)
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Store alert messages to display to the user (success/error notifications)
  const [alerts, setAlerts] = useState<Alert[]>([]);

  // Store field-specific validation errors from the server
  const [errors, setErrors] = useState<Errors>({});

  // This function handles input changes in form fields.
  // It updates the form data and clears any existing error for that field.
  function handleInputChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    const { name, value } = e.target;

    // Update the form data with the new input value
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear any existing error for this field when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  }

  // This function removes all alert messages from the display
  function clearAlerts() {
    setAlerts([]);
  }

  // This function displays a new alert message to the user.
  // Success alerts automatically disappear after 5 seconds.
  function showAlert(type: "success" | "danger", message: string) {
    const newAlert: Alert = {
      id: Date.now(),
      type,
      message,
    };
    setAlerts([newAlert]);

    // Auto-dismiss success alerts after 5 seconds
    if (type === "success") {
      setTimeout(() => {
        setAlerts((prev) => prev.filter((alert) => alert.id !== newAlert.id));
      }, 5000);
    }
  }

  // This function removes a specific alert when the user clicks the close button
  function removeAlert(alertId: number) {
    setAlerts((prev) => prev.filter((alert) => alert.id !== alertId));
  }

  // This function handles form submission.
  // It validates the data, sends it to the server, and handles the response.
  async function handleSubmit(e?: React.FormEvent) {
    if (e) e.preventDefault();

    // Clear any previous errors and alert messages
    setErrors({});
    clearAlerts();

    // Show loading state to prevent multiple submissions
    setIsLoading(true);

    // Trim whitespace from all form fields before sending
    const trimmedData = {
      name: formData.name.trim(),
      email: formData.email.trim(),
      subject: formData.subject.trim(),
      message: formData.message.trim(),
    };

    try {
      // Send the form data to the Django API endpoint
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/addresses/email-us/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(trimmedData),
        }
      );

      // Parse the JSON response from the server
      const data: {
        success: boolean;
        message: string;
        errors?: Errors;
      } = await response.json();

      if (data.success) {
        // Show success message to the user
        showAlert("success", data.message);

        // Reset the form to its initial empty state
        setFormData({
          name: "",
          email: "",
          subject: "",
          message: "",
        });
      } else {
        // Show general error message
        showAlert("danger", data.message);

        // Display field-specific validation errors if they exist
        if (data.errors) {
          setErrors(data.errors);
        }
      }
    } catch (error) {
      // Handle network errors or other unexpected issues
      console.error("Error:", error);
      showAlert(
        "danger",
        "An error occurred while sending your message. Please try again."
      );
    } finally {
      // Always hide the loading state when submission is complete
      setIsLoading(false);
    }
  }

  return (
    <div className="row contact-form-container justify-content-center">
      <div className="col-xl-9 col-lg-12 mt-4">
        {/* Main form container */}
        <div
          className="contact-form shadow-sm p-4"
          style={{
            boxShadow: "0 0 30px rgba(214, 215, 216, 0.6)",
          }}
        >
          {/* Alert Container - displays success/error messages to the user */}
          <div id="contact-form-alert-container">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`alert alert-${alert.type} alert-dismissible fade show text-center`}
                role="alert"
              >
                {alert.message}
                {/* Close button allows users to manually dismiss alerts */}
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => removeAlert(alert.id)}
                  aria-label="Close"
                ></button>
              </div>
            ))}
          </div>

          {/* Name and Email row - arranged side by side on larger screens */}
          <div className="row">
            <div className="col-md-6 form-group">
              {/* Name input field with validation styling and error handling */}
              <input
                type="text"
                name="name"
                id="id_name"
                className={`form-control ${errors.name ? "is-invalid" : ""}`}
                placeholder="Your Name"
                maxLength={100}
                value={formData.name}
                onChange={handleInputChange}
                style={{
                  borderRadius: "0",
                  boxShadow: "none",
                  fontSize: "14px",
                  padding: "10px 15px",
                }}
              />
              {/* Error message display for name field */}
              <div className="invalid-feedback" id="name-error">
                {Array.isArray(errors.name)
                  ? errors.name.join(", ")
                  : errors.name || ""}
              </div>
            </div>
            <div className="col-md-6 form-group mt-3 mt-md-0">
              {/* Email input field with validation styling and error handling */}
              <input
                type="email"
                name="email"
                id="id_email"
                className={`form-control ${errors.email ? "is-invalid" : ""}`}
                placeholder="Your Email"
                value={formData.email}
                onChange={handleInputChange}
                style={{
                  borderRadius: "0",
                  boxShadow: "none",
                  fontSize: "14px",
                  padding: "10px 15px",
                }}
              />
              {/* Error message display for email field */}
              <div className="invalid-feedback" id="email-error">
                {Array.isArray(errors.email)
                  ? errors.email.join(", ")
                  : errors.email || ""}
              </div>
            </div>
          </div>

          {/* Subject field - full width */}
          <div className="form-group mt-3">
            <input
              type="text"
              name="subject"
              id="id_subject"
              className={`form-control ${errors.subject ? "is-invalid" : ""}`}
              placeholder="Subject"
              maxLength={200}
              value={formData.subject}
              onChange={handleInputChange}
              style={{
                borderRadius: "0",
                boxShadow: "none",
                fontSize: "14px",
                padding: "10px 15px",
              }}
            />
            {/* Error message display for subject field */}
            <div className="invalid-feedback" id="subject-error">
              {Array.isArray(errors.subject)
                ? errors.subject.join(", ")
                : errors.subject || ""}
            </div>
          </div>

          {/* Message textarea field - full width with multiple rows */}
          <div className="form-group mt-3">
            <textarea
              name="message"
              id="id_message"
              className={`form-control ${errors.message ? "is-invalid" : ""}`}
              placeholder="Message"
              rows={5}
              value={formData.message}
              onChange={handleInputChange}
              style={{
                borderRadius: "0",
                boxShadow: "none",
                fontSize: "14px",
                padding: "12px 15px",
              }}
            ></textarea>
            {/* Error message display for message field */}
            <div className="invalid-feedback" id="message-error">
              {Array.isArray(errors.message)
                ? errors.message.join(", ")
                : errors.message || ""}
            </div>
          </div>

          {/* Submit button section - centered with loading state handling */}
          <div className="text-center">
            <button
              type="button"
              onClick={handleSubmit}
              disabled={isLoading}
              className="btn btn-primary"
              style={{
                padding: "10px 24px",
                transition: "0.4s",
                opacity: isLoading ? 0.75 : 1,
              }}
            >
              {/* Dynamic button text based on loading state */}
              <span>{isLoading ? "Sending..." : "Send Message"}</span>
              {/* Loading spinner - only shown when form is being submitted */}
              {isLoading && (
                <span
                  className="spinner-border spinner-border-sm ms-2"
                  role="status"
                  aria-hidden="true"
                  style={{
                    animation: "spin 1s linear infinite",
                  }}
                ></span>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Custom CSS for focus states and animations that couldn't be handled with Bootstrap alone */}
      <style jsx>{`
        .form-control:focus {
          border-color: var(--bs-primary) !important;
          box-shadow: none !important;
        }

        .btn-primary:hover {
          background-color: color-mix(
            in srgb,
            var(--bs-primary),
            transparent 25%
          ) !important;
        }

        @keyframes spin {
          0% {
            transform: rotate(0deg);
          }
          100% {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </div>
  );
}

// This component renders a contact form that allows users to send emails.
// It handles form validation, displays error messages, shows loading states,
// and provides user feedback through success/error alerts.
// The form integrates with a Django backend API for email processing.

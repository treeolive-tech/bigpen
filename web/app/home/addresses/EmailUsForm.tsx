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
  id: number;
  type: "success" | "danger";
  message: string;
}

// Define the structure of validation errors returned from the server
interface Errors {
  [key: string]: string | string[];
}

export default function EmailUsForm() {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    subject: "",
    message: "",
  });
  const [isBtnHovered, setIsBtnHovered] = useState(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [errors, setErrors] = useState<Errors>({});

  function handleInputChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  }

  function clearAlerts() {
    setAlerts([]);
  }

  function showAlert(type: "success" | "danger", message: string) {
    const newAlert: Alert = {
      id: Date.now(),
      type,
      message,
    };
    setAlerts([newAlert]);

    if (type === "success") {
      setTimeout(() => {
        setAlerts((prev) => prev.filter((alert) => alert.id !== newAlert.id));
      }, 5000);
    }
  }

  function removeAlert(alertId: number) {
    setAlerts((prev) => prev.filter((alert) => alert.id !== alertId));
  }

  async function handleSubmit(e?: React.FormEvent) {
    if (e) e.preventDefault();

    setErrors({});
    clearAlerts();
    setIsLoading(true);

    const trimmedData = {
      name: formData.name.trim(),
      email: formData.email.trim(),
      subject: formData.subject.trim(),
      message: formData.message.trim(),
    };

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/addresses/email-us/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(trimmedData),
        }
      );

      const data: {
        success: boolean;
        message: string;
        errors?: Errors;
      } = await response.json();

      if (data.success) {
        showAlert("success", data.message);
        setFormData({ name: "", email: "", subject: "", message: "" });
      } else {
        showAlert("danger", data.message);
        if (data.errors) setErrors(data.errors);
      }
    } catch (error) {
      console.error("Error:", error);
      showAlert(
        "danger",
        "An error occurred while sending your message. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="row contact-form-container justify-content-center">
      <div className="col-xl-9 col-lg-12 mt-4">
        <div
          className="contact-form shadow-sm p-4"
          style={{ boxShadow: "0 0 30px rgba(214, 215, 216, 0.6)" }}
        >
          {/* Alerts */}
          <div id="contact-form-alert-container">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`alert alert-${alert.type} alert-dismissible fade show text-center`}
                role="alert"
              >
                {alert.message}
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => removeAlert(alert.id)}
                  aria-label="Close"
                ></button>
              </div>
            ))}
          </div>

          {/* Name + Email */}
          <div className="row">
            <div className="col-md-6 form-group">
              <input
                type="text"
                name="name"
                id="id_name"
                className={`form-control custom-input ${
                  errors.name ? "is-invalid" : ""
                }`}
                placeholder="Your Name"
                maxLength={100}
                value={formData.name}
                onChange={handleInputChange}
              />
              <div className="invalid-feedback" id="name-error">
                {Array.isArray(errors.name)
                  ? errors.name.join(", ")
                  : errors.name || ""}
              </div>
            </div>
            <div className="col-md-6 form-group mt-3 mt-md-0">
              <input
                type="email"
                name="email"
                id="id_email"
                className={`form-control custom-input ${
                  errors.email ? "is-invalid" : ""
                }`}
                placeholder="Your Email"
                value={formData.email}
                onChange={handleInputChange}
              />
              <div className="invalid-feedback" id="email-error">
                {Array.isArray(errors.email)
                  ? errors.email.join(", ")
                  : errors.email || ""}
              </div>
            </div>
          </div>

          {/* Subject */}
          <div className="form-group mt-3">
            <input
              type="text"
              name="subject"
              id="id_subject"
              className={`form-control custom-input ${
                errors.subject ? "is-invalid" : ""
              }`}
              placeholder="Subject"
              maxLength={200}
              value={formData.subject}
              onChange={handleInputChange}
            />
            <div className="invalid-feedback" id="subject-error">
              {Array.isArray(errors.subject)
                ? errors.subject.join(", ")
                : errors.subject || ""}
            </div>
          </div>

          {/* Message */}
          <div className="form-group mt-3">
            <textarea
              name="message"
              id="id_message"
              className={`form-control custom-input textarea-input ${
                errors.message ? "is-invalid" : ""
              }`}
              placeholder="Message"
              rows={5}
              value={formData.message}
              onChange={handleInputChange}
            ></textarea>
            <div className="invalid-feedback" id="message-error">
              {Array.isArray(errors.message)
                ? errors.message.join(", ")
                : errors.message || ""}
            </div>
          </div>

          {/* Submit */}
          <div className="text-center">
            <button
              type="button"
              onClick={handleSubmit}
              onMouseEnter={() => setIsBtnHovered(true)}
              onMouseLeave={() => setIsBtnHovered(false)}
              disabled={isLoading}
              className="btn text-white"
              style={{
                padding: "10px 24px",
                transition: "0.4s",
                opacity: isLoading ? 0.75 : 1,
                backgroundColor: isBtnHovered
                  ? "color-mix(in srgb, var(--bs-primary), transparent 25%)"
                  : "var(--bs-primary)",
              }}
            >
              <span>{isLoading ? "Sending..." : "Send Message"}</span>
              {isLoading && (
                <span
                  className="spinner-border spinner-border-sm ms-2"
                  role="status"
                  aria-hidden="true"
                ></span>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Custom CSS */}
      <style jsx>{`
        .form-control:focus {
          border-color: var(--bs-primary) !important;
          box-shadow: none !important;
        }

        .custom-input {
          border-radius: 0;
          box-shadow: none;
          font-size: 14px;
          padding: 10px 15px;
        }

        .textarea-input {
          padding: 12px 15px;
        }
      `}</style>
    </div>
  );
}

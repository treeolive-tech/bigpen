"use client";

import clsx from "clsx";
import { useEffect, useState } from "react";

export default function BackToTopBtn() {
  const [isVisible, setIsVisible] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    // This function checks the scroll position.
    // If the user has scrolled down more than 100px, the button becomes visible.
    // Otherwise, it stays hidden.
    const toggleBtnVisibilityOnScrollPosition = () => {
      setIsVisible(window.scrollY > 100);
    };

    // Add event listeners for scroll and load.
    // On scroll or when the page loads, we check if the button should be shown.
    window.addEventListener("scroll", toggleBtnVisibilityOnScrollPosition);
    window.addEventListener("load", toggleBtnVisibilityOnScrollPosition);

    // Cleanup: remove the event listeners when the component is removed from the page.
    return () => {
      window.removeEventListener("scroll", toggleBtnVisibilityOnScrollPosition);
      window.removeEventListener("load", toggleBtnVisibilityOnScrollPosition);
    };
  }, []);

  // This function is called when the button is clicked.
  // It prevents the default link behavior and smoothly scrolls the page to the top.
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <a
      id="back-to-top"
      href="#"
      onClick={handleClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        width: "40px",
        height: "40px",
        transition: "all 0.4s",
        backgroundColor: isHovered
          ? "color-mix(in srgb, var(--bs-primary), transparent 20%)"
          : "var(--bs-primary)",
      }}
      className={clsx(
        "d-flex align-items-center justify-content-center position-fixed end-0 bottom-0 mb-3 me-3",
        "rounded z-2",
        { "opacity-1 visible": isVisible, "opacity-0 invisible": !isVisible },
      )}
    >
      <i className="bi bi-arrow-up-short fs-3 text-white"></i>
    </a>
  );
}
// This component is a "Back to Top" button that appears when the user scrolls down the page.

import clsx from "clsx";
import { useEffect, useState } from "react";
import styles from "./BackToTopBtn.module.css";

export default function BackToTopBtn() {
  const [isVisible, setIsVisible] = useState(false);

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
      href="#"
      onClick={handleClick}
      // The className combines:
      // - The CSS module class for styling (.back-to-top)
      // - The "visible" class from the module if the button should be visible
      // - Bootstrap utility classes for positioning and layout
      className={clsx(
        styles["back-to-top"],
        { [styles.visible]: isVisible },
        "d-flex align-items-center justify-content-center position-fixed end-0 bottom-0 mb-3 me-3",
      )}
    >
      <i className="bi bi-arrow-up-short"></i>
    </a>
  );
}
